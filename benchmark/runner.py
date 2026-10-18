"""Bounded execution for locally reviewed candidates; not an OS security sandbox."""
import json
import os
import resource
import signal
import subprocess
import tempfile
from pathlib import Path
from .protocol import ROOT

LIMIT=1024*1024

def _limits():
    os.setsid()
    resource.setrlimit(resource.RLIMIT_FSIZE,(LIMIT,LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU,(10,10))

def run_port(source, values, timeout=15):
    with tempfile.TemporaryDirectory(prefix="legacy-eval-") as temp:
        work=Path(temp)
        (work/"port.ts").write_bytes(source.read_bytes())
        try:
            build=subprocess.run([str(ROOT/"node_modules/.bin/tsc"),str(work/"port.ts"),"--ignoreConfig","--outDir",str(work),"--strict","--target","ES2022","--module","commonjs","--skipLibCheck"],capture_output=True,text=True,timeout=30)
        except subprocess.TimeoutExpired:
            return {"compiled":False,"error":"compiler timeout"},[]
        if build.returncode:return {"compiled":False,"error":(build.stdout+build.stderr)[:6000]},[]
        (work/"run.cjs").write_text("const {evaluate}=require('./port.js'); const fs=require('fs'); for(const input of JSON.parse(fs.readFileSync(0,'utf8'))){try { console.log(JSON.stringify(evaluate(input))); }catch(e){console.log(JSON.stringify({runtimeError:String(e)}));}}")
        with (work/'stdout').open('wb') as out,(work/'stderr').open('wb') as err:
            process=subprocess.Popen(['node',str(work/'run.cjs')],stdin=subprocess.PIPE,stdout=out,stderr=err,preexec_fn=_limits)
            try:
                process.communicate(json.dumps(values).encode(),timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);process.communicate()
                return {"compiled":True,"error":"candidate timeout"},[]
            finally:
                # Remove surviving descendants even after the direct child exits.
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
        stdout=(work/'stdout').read_bytes();stderr=(work/'stderr').read_bytes()
        if len(stdout)>=LIMIT or len(stderr)>=LIMIT:return {"compiled":True,"error":"candidate output limit"},[]
        if process.returncode:return {"compiled":True,"error":stderr.decode(errors='replace')[:6000] or f"exit {process.returncode}"},[]
        try:outputs=[json.loads(line) for line in stdout.splitlines()]
        except (json.JSONDecodeError,UnicodeDecodeError):return {"compiled":True,"error":"non-JSON output"},[]
        if len(outputs)!=len(values):return {"compiled":True,"error":"response count mismatch"},[]
        if any(type(v) is not dict or type(v.get('ok')) is not bool for v in outputs):return {"compiled":True,"error":"invalid response shape"},[]
        return {"compiled":True},outputs

def same_response(left,right):
    """JSON canonical comparison keeps booleans distinct from numeric values."""
    return json.dumps(left,sort_keys=True,separators=(',',':'))==json.dumps(right,sort_keys=True,separators=(',',':'))
