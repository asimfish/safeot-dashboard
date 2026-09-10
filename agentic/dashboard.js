'use strict';
(() => {
  const data = JSON.parse(document.getElementById('cost-data').textContent);
  const defaults = data.price_per_million;
  const inputs = { input: document.getElementById('price-input'), cached: document.getElementById('price-cached'), cache_write: document.getElementById('price-write'), output: document.getElementById('price-output') };
  const scope = document.getElementById('cost-scope');
  const status = document.getElementById('price-state');
  const money = n => new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(n);
  const num = n => n.toLocaleString('en-US');
  const labels = {grasp_bottle:'抓取并稳定保持',place_bottle:'放到圆垫并释放',grasp_beaker100:'抓取烧杯'};
  const cost = (g, p) => ((g.input - g.cached - g.cache_write) * p.input + g.cached * p.cached + g.cache_write * p.cache_write + g.output * p.output) / 1e6;
  function cell(label, text, sub, strong = false) {
    const td = document.createElement('td');
    td.dataset.label = label;
    const main = document.createElement(strong ? 'strong' : 'span'); main.textContent = text; td.append(main);
    if (sub) {const span = document.createElement('span'); span.className = 'sub'; span.textContent = sub; td.append(span);}
    return td;
  }
  function update() {
    const prices = {}; let valid = true;
    Object.entries(inputs).forEach(([key, el]) => {
      const value = el.valueAsNumber;
      const okay = Number.isFinite(value) && value >= 0 && value <= 1000000;
      el.setAttribute('aria-invalid', String(!okay));
      valid = valid && okay; prices[key] = value;
    });
    if (!valid) {status.textContent = '请输入 0—1,000,000 之间的有效单价。金额保留上次有效结果。'; return;}
    const standard = Object.keys(inputs).every(k => prices[k] === defaults[k]);
    status.textContent = standard ? '当前：官方标准价' : '当前：自定义单价；金额仅为估算';
    const groups = data.groups.filter(g => scope.value === 'all' || g.experiment === scope.value);
    const sum = key => groups.reduce((n,g) => n + g[key],0);
    const total = groups.reduce((n,g) => n + cost(g,prices),0);
    const label = scope.value === 'all' ? 'E1—E3' : scope.value;
    document.getElementById('cost-label').textContent = label + ' · 已知用量的 ' + (standard ? 'API 等值估算' : '自定义估算');
    document.getElementById('cost-total').textContent = money(total);
    document.getElementById('cost-input').textContent = num(sum('input'));
    document.getElementById('cost-output').textContent = num(sum('output'));
    document.getElementById('cost-cached').textContent = num(sum('cached'));
    document.getElementById('cost-unknown').textContent = sum('unknown_usage_requests') + ' 次';
    const basis = document.getElementById('cost-basis');
    basis.replaceChildren(document.createTextNode((standard ? '按 API Standard：' : '自定义估算单价：') + `输入 $${prices.input} / 百万、缓存输入 $${prices.cached} / 百万、输出 $${prices.output} / 百万 token。`));
    const source = document.createElement('a'); source.href = data.price_source; source.target = '_blank'; source.rel = 'noopener'; source.textContent = 'OpenAI 官方价格';
    basis.append(source, document.createTextNode(' · 核对于 2026-09-10。'));
    const rows = document.createDocumentFragment();
    groups.forEach(g => {
      const tr = document.createElement('tr');
      const name = (scope.value === 'all' ? g.experiment + ' · ' : '') + g.robot + ' · ' + (g.valid_cohort ? labels[g.task] : '基础设施无效场景');
      tr.append(cell('条件',name,`${g.effort} · ${g.episodes} ${g.valid_cohort ? '集' : '场景'}`,true),cell('输入 token',num(g.input),g.cached ? '含缓存 ' + num(g.cached) : ''),cell('输出 token',num(g.output)),cell('估算 USD',money(cost(g,prices)),null,true),cell('估算 / 集',g.valid_cohort ? money(cost(g,prices)/g.episodes) : '—'));
      rows.append(tr);
    });
    document.getElementById('cost-rows').replaceChildren(rows);
  }
  // Native details remain available without JavaScript; deep links reveal their ancestors.
  function revealHash() {
    let id;
    try {id = decodeURIComponent(location.hash.slice(1));} catch {return;}
    if (!id) return;
    const target = document.getElementById(id); if (!target) return;
    let parent = target.parentElement;
    while (parent) {if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement;}
    if (target.tagName === 'DETAILS') target.open = true;
    requestAnimationFrame(() => target.scrollIntoView({behavior:'instant',block:'start'}));
  }
  Object.values(inputs).forEach(el => el.addEventListener('input',update));
  scope.addEventListener('change',update);
  document.getElementById('price-reset').addEventListener('click',() => {Object.entries(inputs).forEach(([k,el]) => {el.value = defaults[k];}); update();});
  window.addEventListener('hashchange',revealHash);
  update(); revealHash();
})();
