"""Rebuild measured results from the executable oracle and frozen ports."""
import argparse
import hashlib
import json
import platform
import time
from .cases import cases
from .protocol import ROOT,evaluate
from .runner import run_port

def run():
    values=cases()
    expected=[evaluate(v) for v in values]
    rows=[]
    implementations=[('reference','ports/reference/src/port.ts'),('claude-code','variants/claude-code/port.ts'),('codex','variants/codex/port.ts')]
    if (ROOT/'ports/manual/src/port.ts').exists(): implementations.append(('manual','ports/manual/src/port.ts'))
    for name,relative in implementations:
        print(f'evaluating {name}: {len(values)} heldout cases',flush=True)
        source=ROOT/relative
        start=time.monotonic()
        health,outputs=run_port(source,values) if source.exists() else ({'compiled':False,'error':'No generated artifact'},[])
        mismatches=[{'index':i,'input':v,'expected':e,'actual':outputs[i] if i<len(outputs) else None} for i,(v,e) in enumerate(zip(values,expected)) if i>=len(outputs) or outputs[i]!=e]
        provenance_path=source.parent/'provenance.json'
        rows.append({'name':name,'authorship':'agent-authored reference' if name=='reference' else 'participant-supplied manual port' if name=='manual' else 'unmodified CLI generation','cases':len(values),'passed':len(values)-len(mismatches),'parity':round((len(values)-len(mismatches))/len(values)*100,2),'strictCompile':health['compiled'],'evaluationSeconds':round(time.monotonic()-start,3),'lines':len(source.read_text().splitlines()) if source.exists() else None,'sha256':hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None,'health':health,'mismatches':mismatches[:20],'provenance':json.loads(provenance_path.read_text()) if provenance_path.exists() else None})
    report={'schemaVersion':1,'seed':241019,'caseCount':len(values),'caseBreakdown':{'rootAndKeyset':4,'fieldBoundaryAndType':60,'missingKeys':8,'invalidAndOrdering':4,'seededRandom':300,'crossProfileBoundaries':56},'publicExamples':9,'oracle':'legacy/sensor_config.c + strict Python JSON boundary','python':platform.python_version(),'manualBaseline':next((r for r in rows if r['name']=='manual'),None),'manualBaselineReason':'No independently produced human implementation or timed human trial was supplied.','studyLimitations':['One synthetic C program, one attempt per CLI, no statistical generalisation.','CLI model families and tool permissions differ; elapsed time includes service and tool latency.','Claude attempt 1 could not authenticate in bare mode; attempt 2 reached the provider API usage limit. No generated Claude implementation exists.', 'Working directories restrict task inputs by instruction, not by a security sandbox.','Heldout cases are public after the frozen first attempt; repeat runs are contaminated.','Line count and strict compilation are descriptive proxies, not quality scores.','Cost and human effort remain unknown unless independently reported.'],'results':rows}
    (ROOT/'artifacts/report.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'web/public').mkdir(exist_ok=True)
    (ROOT/'web/public/report.json').write_text(json.dumps(report,indent=2)+'\n')
    probes=[{'input':v,'observed':evaluate(v)} for v in values[:64]]
    (ROOT/'artifacts/recovery-probes.json').write_text(json.dumps(probes,indent=2)+'\n')
    print(json.dumps({r['name']:r['passed'] for r in rows}),flush=True)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['run']);parser.parse_args();run()
