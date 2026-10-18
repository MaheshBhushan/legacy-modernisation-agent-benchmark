import json
import subprocess
import tempfile
from pathlib import Path
from .protocol import ROOT

def run_port(source, values):
    with tempfile.TemporaryDirectory(prefix="legacy-eval-") as temp:
        work=Path(temp)
        (work/"port.ts").write_bytes(source.read_bytes())
        build=subprocess.run([str(ROOT/"node_modules/.bin/tsc"),str(work/"port.ts"),"--outDir",str(work),"--strict","--target","ES2022","--module","commonjs","--skipLibCheck"],capture_output=True,text=True,timeout=30)
        if build.returncode:return {"compiled":False,"error":(build.stdout+build.stderr)[:6000]},[]
        (work/"run.cjs").write_text("const {evaluate}=require('./port.js'); const fs=require('fs'); for(const input of JSON.parse(fs.readFileSync(0,'utf8'))){try { console.log(JSON.stringify(evaluate(input))); }catch(e){console.log(JSON.stringify({runtimeError:String(e)}));}}")
        result=subprocess.run(['node',str(work/'run.cjs')],input=json.dumps(values),capture_output=True,text=True,timeout=15)
        if result.returncode:return {"compiled":True,"error":result.stderr[:6000]},[]
        try: outputs=[json.loads(line) for line in result.stdout.splitlines()]
        except json.JSONDecodeError:return {"compiled":True,"error":"non-JSON output"},[]
        return {"compiled":True},outputs
