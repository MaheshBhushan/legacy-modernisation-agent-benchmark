"""Deterministic heldout boundaries, malformed requests, and seeded samples."""
import random
import json
from pathlib import Path
from .protocol import DEFAULT

def cases():
    output=[None,[],{},DEFAULT|{"extra":1}]
    boundaries={"sampleMs":(10,60000),"gain":(1,16),"offsetMilli":(-100000,100000),"rawMilli":(-1000000,1000000),"alarmLowMilli":(-20000000,20000000),"alarmHighMilli":(-20000000,20000000)}
    for key,(lo,hi) in boundaries.items():
        for value in (lo-1,lo,lo+1,hi-1,hi,hi+1,None,True,"1",1.5):
            output.append(DEFAULT|{key:value})
    for key in DEFAULT:
        v=DEFAULT.copy();del v[key];output.append(v)
    output += [DEFAULT|{"sampleMs":9,"gain":False},DEFAULT|{"profile":"other"},DEFAULT|{"enabled":0},DEFAULT|{"alarmLowMilli":80000}]
    rng=random.Random(241019)
    for _ in range(300):
        output.append(DEFAULT|{"profile":rng.choice(['temperature','pressure']),"sampleMs":rng.randint(10,60000),"gain":rng.randint(1,16),"rawMilli":rng.randint(-1000000,1000000),"offsetMilli":rng.randint(-100000,100000),"alarmLowMilli":rng.randint(-100000,0),"alarmHighMilli":rng.randint(1,1200000),"enabled":rng.choice([True,False])})
    for profile in ('temperature','pressure'):
        for raw in (-40001,-40000,-39999,-1,0,1,79999,80000,80001,124999,125000,125001,999999,1000000):
            for enabled in (True,False):output.append(DEFAULT|{"profile":profile,"rawMilli":raw,"enabled":enabled,"sampleMs":11})
    # Evaluation corpus v2 removes overlap with public examples and adds JSON integral-number representations.
    public=[v["input"] for v in json.loads((Path(__file__).resolve().parents[1]/"spec/public-cases.json").read_text())]
    output=[v for v in output if v not in public]
    output += [DEFAULT|{"sampleMs":103.0,"gain":1.0,"offsetMilli":-0.0},DEFAULT|{"sampleMs":1e1,"rawMilli":-0.0},DEFAULT|{"gain":False,"sampleMs":100.0}]
    return output
