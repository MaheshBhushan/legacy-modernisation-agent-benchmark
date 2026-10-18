import tempfile
import unittest
from pathlib import Path
from benchmark.runner import run_port,same_response

class RunnerTests(unittest.TestCase):
    def exercise(self,code,timeout=2):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'port.ts';source.write_text(code)
            return run_port(source,[{}],timeout=timeout)
    def test_boolean_is_not_integer(self):
        self.assertFalse(same_response({'ok':True},{'ok':1}))
    def test_extra_output_is_rejected(self):
        health,_=self.exercise("export function evaluate(_:unknown){console.log('{}');return {ok:true};}")
        self.assertEqual(health['error'],'response count mismatch')
    def test_bad_shape_is_rejected(self):
        health,_=self.exercise("export function evaluate(_:unknown){return {ok:1};}")
        self.assertEqual(health['error'],'invalid response shape')
    def test_timeout_is_recorded(self):
        health,_=self.exercise("export function evaluate(_:unknown){while(true){} }",timeout=.1)
        self.assertEqual(health['error'],'candidate timeout')
    def test_output_limit_is_recorded(self):
        health,_=self.exercise("export function evaluate(_:unknown){return {ok:true,padding:'x'.repeat(2000000)};}")
        self.assertEqual(health['error'],'candidate output limit')
