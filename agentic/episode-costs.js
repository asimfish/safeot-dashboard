'use strict';
(() => {
  const data = JSON.parse(document.getElementById('episode-data').textContent);
  const rows = data.episodes;
  const condition = document.getElementById('episode-condition');
  const result = document.getElementById('episode-result');
  const nf = n => Number(n).toLocaleString('en-US');
  const usd = n => '$' + n.toFixed(4);
  const secs = n => Number.isFinite(n) ? n.toFixed(1) + ' 秒' : '未记录';
  const labels = {grasp_bottle:'抓取',place_bottle:'放置'};
  const stops={model_claimed_done:'模型声明完成，结果看独立评估',geometric_hard_abort:'几何穿透触发中止',request_budget_exhausted:'请求次数耗尽',provider_error_after_one_retry:'网络错误，重试后仍失败',nonretryable_provider_error:'不可重试的服务错误',apparatus_error:'实验装置错误',model_provenance_mismatch:'模型返回来源不匹配',supervisor_stop_before_request:'监督停止后续请求',supervisor_stop_after_response:'返回后监督停止'};
  const key = e => [e.robot,e.task,e.effort].join('|');
  function el(tag,text,cls) {const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
  function cell(label) {const n=el('td');n.dataset.label=label;return n;}
  function line(parent,text) {parent.append(el('span',text,'sub'));}
  function update() {
    const p = Object.fromEntries([['input','price-input'],['cached','price-cached'],['cache_write','price-write'],['output','price-output']].map(([k,id]) => [k,document.getElementById(id).valueAsNumber]));
    if(Object.values(p).some(v=>!Number.isFinite(v)||v<0||v>1000000))return;
    const cost=e=>{const t=e.tokens;return ((t.input-t.cached-t.cache_write)*p.input+t.cached*p.cached+t.cache_write*p.cache_write+t.output*p.output)/1e6;};
    const groups = [...new Set(rows.map(key))];
    const amortized = document.createDocumentFragment();
    groups.forEach(k=>{
      const all=rows.filter(e=>key(e)===k),valid=all.filter(e=>e.valid_cohort),success=valid.filter(e=>e.success).length,total=all.reduce((n,e)=>n+cost(e),0),unknown=all.reduce((n,e)=>n+e.unknown_usage_requests,0),e=all[0];
      const card=el('article');card.append(el('h3',e.robot+' '+labels[e.task]+' · '+e.effort),el('strong',success?usd(total/success):'无成功，无法摊销'),el('p',`${usd(total)} 已知费用 ÷ ${success} 条成功轨迹`),el('p',`${valid.length} 集有效尝试${all.length>valid.length?' ＋ '+(all.length-valid.length)+' 个无效场景':''} · 未知用量 ${unknown} 次`));amortized.append(card);
    });
    document.getElementById('amortized-costs').replaceChildren(amortized);
    const selected=rows.filter(e=>(condition.value==='all'||key(e)===condition.value)&&(result.value==='all'||(result.value==='success'&&e.valid_cohort&&e.success)||(result.value==='failure'&&e.valid_cohort&&!e.success)||(result.value==='invalid'&&!e.valid_cohort)));
    const frag=document.createDocumentFragment();
    selected.forEach(e=>{
      const tr=el('tr');const name=cell('轨迹 / 结果');name.append(el('strong',e.robot+' '+labels[e.task]+' · '+e.effort));line(name,'seed '+e.seed);name.append(el('span',!e.valid_cohort?'基础设施无效':e.success?'成功':'失败','badge '+(e.valid_cohort&&e.success?'good':'warning')));line(name,stops[e.stop_reason]||e.stop_reason||'终态未记录');
      const time=cell('采集 / 仿真时间');time.append(el('strong','墙钟：未记录'));line(time,'仿真总时长 '+secs(e.simulation_time_s));line(time,'其中动作执行 '+secs(e.action_time_s));if(e.first_request_at)line(time,'首请求 '+e.first_request_at.slice(5,19).replace('T',' ')+' (UTC+8)');
      const speed=cell('模型输出 / 等待');speed.append(el('strong',e.output_interval_s?e.output_interval_s.toFixed(1)+' 秒 / 次输出':'输出间隔：—'));line(speed,e.output_interval_s?(1/e.output_interval_s).toFixed(4)+' Hz · 返回事件平均':'不足 2 个可解析动作返回');line(speed,'累计推理等待 '+secs(e.inference_wait_s));line(speed,e.requests+' 次请求 / '+e.model_outputs+' 次动作返回');
      const details=el('details');details.append(el('summary','观测与时序明细'));line(details,e.rgb_observation_sets+' 套四路 RGB＋state，按请求保存');line(details,'观测仿真时刻：[ '+e.request_events.filter(x=>x.has_rgb&&x.observation_sim_time_s!==null).map(x=>Number(x.observation_sim_time_s).toFixed(2)).join(', ')+' ] 秒');line(details,e.observation_interval_sim_s!==null?'观测平均间隔 '+e.observation_interval_sim_s.toFixed(3)+' 仿真秒（非匀速采样）':'观测间隔不可计算');line(details,e.request_interval_s?'调用间隔 '+e.request_interval_s.toFixed(1)+' 墙钟秒（请求开始事件）':'调用间隔不可计算');line(details,'视频 '+(e.video_frames_per_camera??'未记录')+' 帧 / 相机，15 fps 仿真时间');speed.append(details);
      const money=cell('Token / API 等值');money.append(el('strong',usd(cost(e))));line(money,'输入 '+nf(e.tokens.input)+' / 输出 '+nf(e.tokens.output));line(money,'缓存命中 '+nf(e.tokens.cached)+' / 写入 '+nf(e.tokens.cache_write));line(money,e.tokens.known_requests+' 次已知用量 · '+e.unknown_usage_requests+' 次未知');if(e.unknown_usage_requests)line(money,'金额不完整；未知用量不按 0 计费');tr.append(name,time,speed,money);frag.append(tr);
    });
    document.getElementById('episode-rows').replaceChildren(frag);
    document.getElementById('episode-summary').textContent=`显示 ${selected.length} 条：${selected.filter(e=>e.valid_cohort&&e.success).length} 成功、${selected.filter(e=>e.valid_cohort&&!e.success).length} 有效失败、${selected.filter(e=>!e.valid_cohort).length} 无效场景。已知费用 ${usd(selected.reduce((n,e)=>n+cost(e),0))}；未知 usage ${selected.reduce((n,e)=>n+e.unknown_usage_requests,0)} 次。`;
  }
  condition.addEventListener('change',update);result.addEventListener('change',update);
  for(const id of ['price-input','price-cached','price-write','price-output'])document.getElementById(id).addEventListener('input',update);
  document.getElementById('price-reset').addEventListener('click',update);
  update();
})();
