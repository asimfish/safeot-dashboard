import json, glob, os, statistics as st, sys
ROOT='/home/liyufeng'
EXPS=[
 ('E1','PsiBot','grasp_beaker100','astra_psibot_grasp',['artifacts/phase2_campaign05_calibrated','artifacts/phase2_campaign05_transport_resume']),
 ('E2','FR3','grasp_bottle','astra_fr3_grasp_e2',['artifacts/phase2_paired01','artifacts/phase2_paired02_resume']),
 ('E2','PsiBot','grasp_bottle','astra_psibot_grasp_e2',['artifacts/post_reboot_full01/paired','artifacts/post_reboot_full02/paired']),
 ('E3','FR3','grasp_bottle','astra_fr3_grasp_e3',['artifacts/phase2_grasp_01']),
 ('E3','FR3','place_bottle','astra_fr3_grasp_e3',['artifacts/phase2_place_01','artifacts/phase2_place_02_resume']),
 ('E3','PsiBot','grasp_bottle','astra_psibot_grasp_e3',['artifacts/e3_full02/paired','artifacts/e3_resume_full01/paired']),
]
INVALID={'E3/PsiBot':{'9205','9206','9207','9208'}}
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def mean(x): return round(st.mean(x),3) if x else None
out={'groups':[], 'schemas':{}, 'state_keys':{}, 'cameras':{}}
for exp,robot,task,d,subs in EXPS:
    eps=[]
    for sub in subs:
        for ev in sorted(glob.glob(f'{ROOT}/{d}/{sub}/episode_*/evaluation.json')):
            epdir=os.path.dirname(ev); e=load(ev) or {}
            name=os.path.basename(epdir); seed=name.split('seed_')[1].split('_')[0] if 'seed_' in name else name
            effort=e.get('effort') or ('xhigh' if exp=='E1' else name.split('_')[-1])
            acts=[]; durs=[]; lat=[]; ntool=0; req_usage=[]
            decs=sorted(glob.glob(f'{epdir}/decision_*'))
            for dd in decs:
                c=load(f'{dd}/model/candidate.json')
                if c is None:
                    # E1 layout fallback
                    for alt in glob.glob(f'{dd}/**/candidate.json',recursive=True)+glob.glob(f'{dd}/**/function_arguments.json',recursive=True)+glob.glob(f'{dd}/**/tool_arguments.json',recursive=True):
                        c=load(alt); 
                        if c: break
                if c and isinstance(c,dict) and 'actions' in c:
                    acts.append(len(c['actions'])); durs+= [a.get('duration_s') for a in c['actions'] if isinstance(a,dict) and a.get('duration_s') is not None]
                pm=load(f'{dd}/model/provenance.json') or load(f'{dd}/model/response_metadata.json') or {}
                if pm.get('elapsed_s') is not None: lat.append(pm['elapsed_s'])
                u=pm.get('usage') or {}
                if u.get('input_tokens') is not None:
                    req_usage.append((u.get('input_tokens'),u.get('output_tokens'),((u.get('output_tokens_details') or {}).get('reasoning_tokens')),pm.get('elapsed_s')))
            def num(v): return len(v) if isinstance(v,list) else v
            eps.append(dict(seed=seed,effort=effort,success=e.get('success'),stop=e.get('stop_reason'),
                decisions=num(e.get('decisions')),requests=num(e.get('requests')),max_lift_mm=round((e.get('max_lift_m') or 0)*1000,1),
                lifted50=e.get('lifted_at_least_50mm') if e.get('lifted_at_least_50mm') is not None else ((e.get('max_lift_m') or 0)>=0.05),sim_s=num(e.get('simulation_time_s')),action_s=num(e.get('action_time_s')),infer_s=num(e.get('total_inference_s')),
                n_actions=sum(acts) if acts else None,n_dec_dirs=len(decs),dur_mean=mean(durs),dur_list=durs,lat_mean=mean(lat),
                in_tok=e.get('input_tokens'),out_tok=e.get('output_tokens'),req_usage=req_usage,ev_keys=sorted(e.keys()) if not eps else None))
    # schema/state/cameras sample from last decision with files
    for ep in reversed(eps):
        pass
    sample=None
    for sub in subs:
        cands=sorted(glob.glob(f'{ROOT}/{d}/{sub}/episode_*/decision_*/model/schema.json'))
        if cands: sample=cands[-1]; break
    key=f'{exp}/{robot}/{task}'
    if sample:
        out['schemas'][key]=load(sample)
        ps=load(os.path.join(os.path.dirname(os.path.dirname(sample)),'observation','public_state.json')) or {}
        def keys(o,pre=''):
            r=[]
            if isinstance(o,dict):
                for k,v in o.items():
                    if isinstance(v,dict) and k!='cameras': r+=keys(v,pre+k+'.')
                    else: r.append(pre+k)
            return r
        out['state_keys'][key]=keys(ps)
        cams=ps.get('cameras') or {}
        out['cameras'][key]={k:(v.get('resolution_wh') if isinstance(v,dict) else None) for k,v in cams.items()}
        obs=os.path.join(os.path.dirname(os.path.dirname(sample)),'observation')
        out['cameras'][key]['_files']=sorted(os.listdir(obs)) if os.path.isdir(obs) else None
        out['cameras'][key]['_task_instruction']=ps.get('task_instruction')
    else:
        # E1 fallback: list a decision dir
        dd=sorted(glob.glob(f'{ROOT}/{d}/{subs[0]}/episode_*/decision_*'))
        out['cameras'][key]={'_decision_dir_listing': sorted(os.listdir(dd[-1])) if dd else None, '_dir':dd[-1] if dd else None}
    # groups by effort
    inv=INVALID.get(f'{exp}/{robot}',set())
    for eff in sorted(set(x['effort'] for x in eps)):
        g=[x for x in eps if x['effort']==eff and x['seed'] not in inv]
        ginv=[x for x in eps if x['effort']==eff and x['seed'] in inv]
        def m(k): 
            v=[x[k] for x in g if x.get(k) is not None]; return mean(v)
        tot_act=sum(x['n_actions'] or 0 for x in g); tot_act_s=sum(x['action_s'] or 0 for x in g); tot_sim=sum(x['sim_s'] or 0 for x in g); tot_inf=sum(x['infer_s'] or 0 for x in g)
        tot_req=sum(x['requests'] or 0 for x in g)
        out['groups'].append(dict(exp=exp,robot=robot,task=task,effort=eff,N=len(g),N_invalid=len(ginv),
            success=sum(1 for x in g if x['success']),lifted50=sum(1 for x in g if x['lifted50']),
            mean_decisions=m('decisions'),mean_requests=m('requests'),mean_actions=m('n_actions'),
            actions_per_decision=round(tot_act/max(1,sum(x['n_dec_dirs'] for x in g)),2),
            mean_action_dur_s=mean([dv for x in g for dv in x['dur_list']]),
            mean_sim_s=m('sim_s'),mean_action_s=m('action_s'),mean_infer_s=m('infer_s'),
            mean_latency_s=round(tot_inf/tot_req,2) if tot_req else None,
            waypoints_per_sim_min=round(60*tot_act/tot_act_s,2) if tot_act_s else None,
            decisions_per_wall_min=round(60*sum(x['decisions'] or 0 for x in g)/(tot_inf+tot_act),3) if (tot_inf+tot_act) else None,
            wall_per_episode_s=round((tot_inf+tot_act)/max(1,len(g)),1),
            mean_in_tok=m('in_tok'),mean_out_tok=m('out_tok'),
            req_stats=(lambda R: dict(n=len(R),in_mean=mean([r[0] for r in R]),in_med=(st.median([r[0] for r in R]) if R else None),out_mean=mean([r[1] for r in R]),out_med=(st.median([r[1] for r in R]) if R else None),
                reason_mean=mean([r[2] for r in R if r[2] is not None]),reason_share=(round(sum(r[2] for r in R if r[2] is not None)/max(1,sum(r[1] for r in R if r[2] is not None)),3) if R else None),
                lat_med=(st.median([r[3] for r in R if r[3] is not None]) if R else None),lat_min=(min(r[3] for r in R if r[3] is not None) if R else None),lat_max=(max(r[3] for r in R if r[3] is not None) if R else None)))([r for x in g for r in x['req_usage']]),
            ep_tok=(lambda T: dict(mean=mean(T),min=min(T) if T else None,max=max(T) if T else None))([ (x['in_tok'] or 0)+(x['out_tok'] or 0) for x in g if x['in_tok'] is not None]),
            episodes=[{k:v for k,v in x.items() if k not in ('dur_list','ev_keys','req_usage')} for x in g],
            invalid=[{k:v for k,v in x.items() if k not in ('dur_list','ev_keys','req_usage')} for x in ginv]))
    if eps and eps[0].get('ev_keys'): out.setdefault('ev_keys',{})[key]=eps[0]['ev_keys']
json.dump(out,open('/tmp/astra_stats.json','w'),ensure_ascii=False,indent=1)
for g in out['groups']:
    print(f"{g['exp']:3}{g['robot']:7}{g['task']:16}{g['effort']:7} N={g['N']:2} ok={g['success']:2} lift50={g['lifted50']:2} dec={g['mean_decisions']} act={g['mean_actions']} a/d={g['actions_per_decision']} dur={g['mean_action_dur_s']} sim={g['mean_sim_s']} act_s={g['mean_action_s']} inf={g['mean_infer_s']} lat={g['mean_latency_s']} wp/simmin={g['waypoints_per_sim_min']} dec/wallmin={g['decisions_per_wall_min']} wall/ep={g['wall_per_episode_s']} tok={g['mean_in_tok']}/{g['mean_out_tok']}")
for g in out['groups']:
    r=g['req_stats']; t=g['ep_tok']
    print(f"TOK {g['exp']} {g['robot']} {g['task']} {g['effort']}: req n={r['n']} in {r['in_mean']}/{r['in_med']} out {r['out_mean']}/{r['out_med']} reason {r['reason_mean']} share {r['reason_share']} lat med {r['lat_med']} [{r['lat_min']},{r['lat_max']}] | ep tok mean {t['mean']} [{t['min']},{t['max']}]")
print('CAMERAS',json.dumps(out['cameras'],ensure_ascii=False))
print('STATE_KEYS',json.dumps(out['state_keys'],ensure_ascii=False))
print('EV_KEYS',json.dumps(out.get('ev_keys'),ensure_ascii=False))
