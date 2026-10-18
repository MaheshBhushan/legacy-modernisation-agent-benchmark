import copy
import json
import subprocess
import unittest
from benchmark.protocol import DEFAULT, ROOT, evaluate
from benchmark.cases import cases
from benchmark.runner import run_port

class OracleTests(unittest.TestCase):
    def test_public_examples(self):
        for case in json.loads((ROOT/'spec/public-cases.json').read_text()):
            self.assertEqual(evaluate(case['input']),case['expected'])
    def test_canonical_multi_error(self):
        self.assertEqual(evaluate(DEFAULT|{'sampleMs':9,'gain':False})['error']['field'],'sampleMs')
        self.assertEqual(evaluate(DEFAULT|{'gain':False,'extra':1})['error']['field'],'$')
    def test_round_clamp_disable_order(self):
        value=evaluate(DEFAULT|{'sampleMs':11,'rawMilli':1000000,'enabled':False})
        self.assertEqual(value['warnings'],['sample-rounded','reading-clamped'])
        self.assertEqual(value['status'],'disabled')
    def test_alarm_equality_is_ok(self):
        self.assertEqual(evaluate(DEFAULT|{'rawMilli':80000})['status'],'ok')
    def test_reference_matches_oracle_and_preserves_input(self):
        values=cases();before=copy.deepcopy(values)
        health,actual=run_port(ROOT/'ports/reference/src/port.ts',values)
        self.assertTrue(health['compiled'],health)
        self.assertEqual(actual,[evaluate(v) for v in values])
        self.assertEqual(values,before)
    def test_sanitized_oracle(self):
        target=ROOT/'build/oracle-sanitized'
        subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-pedantic','-fsanitize=address,undefined','-fno-omit-frame-pointer','legacy/sensor_config.c','-o',str(target)],cwd=ROOT,check=True)
        for value in (DEFAULT,DEFAULT|{'rawMilli':1000000,'gain':16,'offsetMilli':100000},DEFAULT|{'rawMilli':-1000000,'gain':16,'offsetMilli':-100000}):
            self.assertEqual(evaluate(value,target),evaluate(value))

if __name__=='__main__':unittest.main()
