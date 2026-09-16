"""Bounded, idle-aware research continuation; never starts experiment workers itself."""
import fcntl
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
BASE = 'https://memory.whalent.com/pt/public/conversation'


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2))
    tmp.replace(path)


def clean(value):
    return re.sub(r'Bearer\s+[^\s"\']+', 'Bearer [REDACTED]', str(value))


def external_steering(message, campaign_id):
    return message.get('type') == 'human' and ('[campaign=' + campaign_id + ';') not in message.get('text', '')


def decide(now, deadline, status, queue, ready, next_at, unresolved=False):
    if now >= deadline:
        return 'deadline'
    if unresolved:
        return 'uncertain_delivery'
    if not ready:
        return 'preparing'
    if status.get('is_running'):
        return 'stream'
    if queue.get('items'):
        return 'respect_queue'
    if now < next_at:
        return 'cooldown'
    return 'dispatch'


class API:
    def __init__(self):
        self.headers = {'Authorization': 'Bearer ' + os.environ['SAFEOT_GUIDANCE_TOKEN'],
                        'Content-Type': 'application/json'}

    def json(self, path, payload=None):
        req = urllib.request.Request(BASE + path, headers=self.headers,
                                     data=None if payload is None else json.dumps(payload, ensure_ascii=False).encode())
        with urllib.request.urlopen(req, timeout=35) as r:
            return json.load(r)

    def stream(self, after_id, seconds=45):
        req = urllib.request.Request(BASE + f'/stream?after_id={after_id}&timeout={seconds}', headers=self.headers)
        with urllib.request.urlopen(req, timeout=seconds + 10) as r:
            event = ''
            for raw in r:
                line = raw.decode().strip()
                if line.startswith('event:'):
                    event = line[6:].strip()
                elif line.startswith('data:'):
                    try:
                        yield event, json.loads(line[5:])
                    except ValueError:
                        continue


def snapshot():
    """File-only observations; PASS strings are not scientific verification."""
    r = ROOT.parents[1] / 'diagnostic_runs/deployment_pathwise/v1'
    out = {}
    for name in ['closed_loop_gate.json', 'mirror_gate.json', 'actor_gradient_gate.json',
                 'campaign_state.json', 'result_summary.json', 'controller_manifest.json']:
        p = r / name
        if p.exists():
            try:
                x = json.loads(p.read_text())
                out[name] = {k: x.get(k) for k in ['status', 'actual_env_step_calls', 'phase', 'jobs'] if k in x}
                out[name]['mtime'] = p.stat().st_mtime
            except (ValueError, OSError):
                out[name] = {'parse_error': True}
    return out


def main():
    lock = (ROOT / 'supervisor.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    cfg = json.loads((ROOT / 'config.json').read_text())
    statefile = ROOT / 'supervisor_state.json'
    st = json.loads(statefile.read_text()) if statefile.exists() else {
        'round': 0, 'last_id': cfg['after_id'], 'next_at': 0, 'submissions': [],
        'unresolved_delivery': False, 'errors': 0, 'started_at': cfg['start_epoch']}
    api = API()
    stop = ROOT / 'STOP'

    def event(kind, **kw):
        with (ROOT / 'events.jsonl').open('a') as f:
            f.write(json.dumps({'at': time.time(), 'kind': kind, **kw}, ensure_ascii=False) + '\n')

    def save(phase, **kw):
        st.update(phase=phase, pid=os.getpid(), heartbeat=time.time(), deadline=cfg['deadline_epoch'], **kw)
        atomic(statefile, st)

    save('waiting_protocol')
    while not stop.exists():
        now = time.time()
        if now >= cfg['deadline_epoch']:
            save('dispatch_window_closed', note='No further submissions; already admitted bounded workers may finish.')
            event('deadline')
            return
        if not (ROOT / 'READY').exists():
            save('waiting_protocol')
            time.sleep(min(15, cfg['deadline_epoch'] - now))  # detached process only
            continue
        if st.get('unresolved_delivery'):
            save('uncertain_delivery', note='No retry: inspect recorded request id and destination before resuming.')
            return
        # Scheduled idle wakeups are distinct from monitoring a running AI.
        if now < st.get('next_at', 0) and not st.get('remote_status', {}).get('is_running'):
            save('scheduled_continuation')
            time.sleep(min(30, st['next_at'] - now, cfg['deadline_epoch'] - now))
            continue
        try:
            status = api.json('/status')
            save('observing', remote_status=status, artifacts=snapshot())
            if status.get('is_running'):
                for typ, value in api.stream(st['last_id'], seconds=min(45, max(1, int(cfg['deadline_epoch'] - time.time())))):
                    if typ == 'message':
                        m = value.get('message', value)
                        mid = int(m.get('id', 0))
                        if mid <= st['last_id']:
                            continue
                        st['last_id'] = mid
                        if external_steering(m, cfg['campaign_id']):
                            save('paused_for_external_steering', steering_message_id=mid)
                            event('external_steering', id=mid)
                            return
                        if m.get('type') in ['ai', 'tool_call', 'tool_result']:
                            event('message', id=mid, type=m.get('type'), text=clean(m.get('text', '') if m.get('type') == 'ai' else m.get('tool_summary', ''))[:3000])
                    elif typ in ['status', 'done']:
                        save('observing_running_agent', remote_status=value)
                continue
            queue = api.json('/queue')
            action = decide(time.time(), cfg['deadline_epoch'], status, queue, True, st['next_at'])
            if action == 'deadline':
                continue
            if action == 'respect_queue':
                event('queue_not_modified', count=len(queue['items']))
                st['next_at'] = time.time() + 120
                save('queued_user_work')
                continue
            if action == 'cooldown':
                save('scheduled_continuation')
                continue
            if st['round'] >= cfg['max_rounds']:
                save('submission_cap_reached')
                return
            round_no = st['round'] + 1
            message = (ROOT / ('initial_guidance.txt' if round_no == 1 else 'continuation_guidance.txt')).read_text()
            message = message.replace('{round}', str(round_no)).replace('{deadline_cst}', cfg['deadline_cst'])
            message += '\n[campaign=' + cfg['campaign_id'] + '; round=' + str(round_no) + ']'
            message += '\n本轮文件快照（仅表示存在，不代表PASS）：\n' + json.dumps(snapshot(), ensure_ascii=False)
            reverse_ok = False
            try:
                rev = api.json('/reverse-token', {'expires_hours': min(6, max(1, (cfg['deadline_epoch'] - time.time()) / 3600))})
                if rev.get('token'):
                    reverse_ok = True
                    message += '\n如需向导师提问或汇报进展，可调用一次性回信接口（' + str(rev.get('expires_at')) + '前有效，仅可成功提交一次）：\n'
                    message += 'curl -X POST "' + rev['submit_url'] + '" -H "Authorization: Bearer ' + rev['token'] + '" -H "Content-Type: application/json" -d \'{"text":"你的提问或进展汇报","sender":"guided-agent"}\''
            except urllib.error.HTTPError as e:
                event('reverse_channel_unavailable', http_status=e.code)
            client_id = cfg['campaign_id'] + f'-r{round_no:02d}'
            st['unresolved_delivery'] = True
            st['pending_client_id'] = client_id
            save('submitting')  # write-ahead receipt, so a crash never blindly replays a POST
            try:
                receipt = api.json('/submit', {'text': message, 'sender': 'senior-guidance',
                                              'execute': True, 'client_message_id': client_id})
            except Exception as e:
                event('submission_uncertain', client_id=client_id, error=clean(e))
                save('uncertain_delivery')
                return
            if not receipt.get('ok'):
                save('submission_rejected', response=receipt)
                return
            st['unresolved_delivery'] = False
            st.pop('pending_client_id', None)
            st['round'] = round_no
            st['submissions'].append({'client_message_id': client_id, 'submitted_at': receipt['submitted_at'],
                                     'reverse_channel_attached': reverse_ok, 'message_id': receipt.get('message_id')})
            atomic(ROOT / f'receipt_{round_no:02d}.json', receipt)
            event('guidance_submitted', client_id=client_id, submitted_at=receipt['submitted_at'])
            st['next_at'] = 0
            save('awaiting_execution')
            # Persisted evidence of receipt; delivery is never counted as a completed experiment.
            seen_running = False
            for typ, value in api.stream(st['last_id'], seconds=45):
                if typ == 'message':
                    m = value.get('message', value); mid = int(m.get('id', 0))
                    if mid <= st['last_id']:
                        continue
                    st['last_id'] = mid
                    if external_steering(m, cfg['campaign_id']):
                        save('paused_for_external_steering', steering_message_id=mid)
                        event('external_steering', id=mid)
                        return
                    if m.get('type') in ['ai', 'tool_call', 'tool_result']:
                        event('message', id=mid, type=m.get('type'), text=clean(m.get('text', '') if m.get('type') == 'ai' else m.get('tool_summary', ''))[:3000])
                elif typ in ['status', 'done']:
                    seen_running |= bool(value.get('is_running'))
                    save('awaiting_execution', remote_status=value, observed_running=seen_running)
            # A fixed 20-minute rhythm prevents repeated nudges and model-capacity retry storms.
            st['next_at'] = max(time.time(), receipt['submitted_at'] / 1000 + cfg['interval_seconds'])
            save('scheduled_continuation')
        except Exception as e:
            st['errors'] += 1
            event('read_transport_error', error=clean(e), count=st['errors'])
            if st['errors'] >= 12:
                save('transport_failure_limit')
                return
            st['next_at'] = min(cfg['deadline_epoch'], time.time() + 60)
            save('transport_backoff')
    save('stopped_by_marker')


if __name__ == '__main__':
    main()
