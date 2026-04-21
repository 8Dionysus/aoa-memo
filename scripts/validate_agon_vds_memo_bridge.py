from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'generated'/'agon_vds_memo_bridge_registry.min.json'
def validate():
    d=json.loads(REGISTRY.read_text(encoding='utf-8'))
    assert d['registry_id']=='agon.vds_memo_bridge.registry.v1'
    assert d['wave']=='XI' and d['live_protocol'] is False and d['runtime_effect']=='none'
    assert d['intake_count']>=4
    ids=[]
    for item in d['intakes']:
        assert item.get('must_not_emit')
        assert item.get('may_emit') is not None

    for item in d['intakes']:
        assert item['durable_write_allowed'] is False
        assert 'durable_scar' not in item.get('may_emit', [])
    assert 'no_durable_scar_write' in d['stop_lines']
    return d
if __name__=='__main__':
    d=validate(); print('validated {count} VDS memo intakes'.format(count=d['intake_count']))
