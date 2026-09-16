import json,torch

def recorded_raw(source,cycle):
 rows=[json.loads(l) for l in (source/'training_episodes.jsonl').read_text().splitlines()];eps=[x for x in rows if x['phase']=='exploration' and x['cycle']==cycle];assert len(eps)==20 and all(len(e['trace'])==12 for e in eps)
 return torch.tensor([x['raw_reward'] for e in eps for x in e['trace']],dtype=torch.float32),torch.tensor([x['penalty'] for e in eps for x in e['trace']],dtype=torch.float32)
