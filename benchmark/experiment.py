"""Run one frozen, no-feedback CLI attempt per tool in isolated task folders."""

import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .protocol import ROOT


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(tool):
    target = ROOT / "variants" / tool
    with tempfile.TemporaryDirectory(prefix="legacy-task-") as temp:
        work = Path(temp)
        for name in ("AGENT_TASK.md", "contract.json", "public-cases.json"):
            shutil.copyfile(ROOT / "spec" / name, work / name)
        prompt = "Read AGENT_TASK.md, contract.json, and public-cases.json in this directory. Implement the requested port.ts now. Do not read paths outside this directory. Do not run tests or inspect benchmark files. Finish after writing port.ts."
        # SECURITY: the recorded claude-code attempt ran with
        # --permission-mode bypassPermissions. In that mode --allowedTools does
        # NOT restrict anything: Bash, WebFetch and every other tool stay
        # available, and the CLI inherits this process's full environment. The
        # "do not read outside this directory" rule is a prompt instruction,
        # not a sandbox. Inputs are this repo's own spec files, so the risk is
        # limited to someone editing spec/ (or a model going off-script).
        # These flags are part of the published method and are left unchanged
        # so reruns stay comparable. benchmark/limit_exec.py's rlimits
        # (10 s CPU, 1 MiB files) are sized for candidate code, not for an
        # agent CLI, so this command is not wrapped in them. Run retries in a
        # throwaway VM or container with no credentials beyond the CLI login.
        command = (
            [
                "claude",
                "--print",
                "--output-format",
                "json",
                "--permission-mode",
                "bypassPermissions",
                "--allowedTools",
                "Read,Write,Edit",
                "--model",
                "sonnet",
                prompt,
            ]
            if tool == "claude-code"
            else [
                "codex",
                "exec",
                "--skip-git-repo-check",
                "--sandbox",
                "workspace-write",
                "--model",
                "gpt-6.1-sol",
                "-c",
                'model_reasoning_effort="medium"',
                "--json",
                prompt,
            ]
        )
        print(f"{tool}: starting isolated frozen attempt", flush=True)
        start = time.monotonic()
        try:
            result = subprocess.run(command, cwd=work, capture_output=True, timeout=300)
            stdout, stderr, code = result.stdout, result.stderr, result.returncode
            outcome = "completed" if code == 0 else "cli-error"
        except subprocess.TimeoutExpired as error:
            stdout, stderr, code = error.stdout or b"", error.stderr or b"", None
            outcome = "timeout"
        (target / "stdout.jsonl").write_bytes(stdout)
        (target / "stderr.log").write_bytes(stderr)
        if (work / "port.ts").exists():
            shutil.copyfile(work / "port.ts", target / "port.ts")
        metadata = {
            "tool": tool,
            "command": command,
            "elapsedSeconds": round(time.monotonic() - start, 3),
            "exitCode": code,
            "outcome": outcome,
            "costUsd": None,
            "humanMinutes": None,
            "inputHashes": {
                p.name: sha(p) for p in sorted(work.iterdir()) if p.name != "port.ts"
            },
            "artifactSha256": sha(target / "port.ts")
            if (target / "port.ts").exists()
            else None,
            "isolation": "separate temporary working directory; instruction boundary, not security isolation",
            "attempt": 2 if tool == "claude-code" else 1,
            "feedbackRepairs": 0,
        }
        (target / "provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(
            f"{tool}: {outcome}; port present={bool(metadata['artifactSha256'])}",
            flush=True,
        )


if __name__ == "__main__":
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, ("claude-code", "codex")))
