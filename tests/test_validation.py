import json, tempfile, unittest, importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"scripts/validate_evaluation.py"
spec=importlib.util.spec_from_file_location("v",p); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
class EvaluationValidationTests(unittest.TestCase):
    def setUp(self): self.d=Path(__file__).parents[1]/"data"
    def test_repository_data_is_valid(self): self.assertEqual(v.validate(self.d/"tasks.json",self.d/"trajectories.json",self.d/"evaluations.json"),[])
    def test_invalid_rating_is_reported(self):
        ev=json.loads((self.d/"evaluations.json").read_text()); ev[0]["overall"]["final_rating"]="excellent"
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            for n in ["tasks.json","trajectories.json"]: td.joinpath(n).write_text((self.d/n).read_text())
            td.joinpath("evaluations.json").write_text(json.dumps(ev))
            self.assertTrue(any("invalid final_rating" in x for x in v.validate(td/"tasks.json",td/"trajectories.json",td/"evaluations.json")))
if __name__=="__main__": unittest.main()
