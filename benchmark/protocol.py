"""Strict JSON trust boundary shared by C oracle callers."""
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("profile", "sampleMs", "gain", "offsetMilli", "rawMilli", "alarmLowMilli", "alarmHighMilli", "enabled")
DEFAULT = dict(profile="temperature", sampleMs=100, gain=1, offsetMilli=0, rawMilli=22000, alarmLowMilli=0, alarmHighMilli=80000, enabled=True)
def invalid(field):
    return {"ok": False, "error": {"code": "INVALID_REQUEST", "field": field}}
def evaluate(value, executable=None):
    if type(value) is not dict or set(value) != set(FIELDS):
        return invalid("$")
    for field in FIELDS:
        expected = str if field == "profile" else bool if field == "enabled" else int
        if type(value[field]) is not expected:
            return invalid(field)
    args = [str(value[f]) if f != "enabled" else str(int(value[f])) for f in FIELDS]
    # Only bounded numeric tokens and profile strings enter the C process.
    if value["profile"] not in ("temperature", "pressure"):
        return invalid("profile")
    for field in FIELDS[1:-1]:
        if abs(value[field]) > 20000000:
            return invalid(field)
    result = subprocess.run([str(executable or ROOT / "build/oracle"), *args], capture_output=True, timeout=2, check=True)
    if len(result.stdout) > 4096:
        raise RuntimeError("oracle output exceeded 4096 bytes")
    return json.loads(result.stdout)
