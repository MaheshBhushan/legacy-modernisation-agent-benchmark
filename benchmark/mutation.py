"""Check whether heldout cases detect named behavioral faults in the reference."""
import json
import tempfile
from pathlib import Path
from .cases import cases
from .protocol import ROOT, evaluate
from .runner import run_port

def run():
    original=(ROOT/'ports/reference/src/port.ts').read_text()
    changes={
        'sample-rounds-down':('Math.ceil(n[\'sampleMs\']!/10)','Math.floor(n[\'sampleMs\']!/10)'),
        'upper-alarm-inclusive':("readingMilli>n['alarmHighMilli']!","readingMilli>=n['alarmHighMilli']!"),
        'disabled-priority-lost':("!v['enabled']?'disabled'","false?'disabled'"),
        'temperature-clamp-off-by-one':("?125000:1000000","?125001:1000000"),
        'warning-order-reversed':('status:!v[','status:!v['),
    }
    values=cases();expected=[evaluate(v) for v in values];results=[]
    for name,(old,new) in changes.items():
        if name=='warning-order-reversed':
            mutated=original.replace('status:!v[','status:!v[').replace('warnings};','warnings:warnings.reverse()};')
        else:
            assert old in original,name
            mutated=original.replace(old,new)
        with tempfile.TemporaryDirectory(prefix='legacy-mutation-') as temp:
            source=Path(temp)/'port.ts';source.write_text(mutated)
            health,actual=run_port(source,values)
        detected=sum(a!=b for a,b in zip(actual,expected))
        results.append({'mutation':name,'compiled':health['compiled'],'detectedCases':detected,'killed':health['compiled'] and detected>0})
    report={'scope':'Five deliberately injected faults in the agent-authored reference; suite sensitivity only, not a general mutation coverage estimate.','mutations':results,'killed':sum(r['killed'] for r in results),'total':len(results)}
    (ROOT/'artifacts/mutation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
    return report
if __name__=='__main__':run()
