#!/usr/bin/env python3
import argparse, json
from pathlib import Path
REQ={"step","consistency","action_match","reasonable","intended_effect"}
ALLOWED={"pass","pass_with_minor_issue","fail"}
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def validate(tasks_path, trajectories_path, evaluations_path):
    tasks={x["task_id"]:x for x in load(tasks_path)}
    trs={(x["task_id"],x["trajectory_id"]):x for x in load(trajectories_path)}
    evs=load(evaluations_path); errors=[]
    for e in evs:
        key=(e.get("task_id"),e.get("trajectory_id"))
        if key[0] not in tasks: errors.append(f"{key}: task_id does not exist in tasks.json"); continue
        if key not in trs: errors.append(f"{key}: matching trajectory does not exist"); continue
        expected=[s["step"] for s in trs[key]["steps"]]
        actual=[s.get("step") for s in e.get("step_evaluations",[])]
        if expected!=actual: errors.append(f"{key}: evaluated steps {actual} do not match trajectory steps {expected}")
        for s in e.get("step_evaluations",[]):
            missing=REQ-s.keys()
            if missing: errors.append(f"{key} step {s.get('step')}: missing fields {sorted(missing)}")
        rating=e.get("overall",{}).get("final_rating")
        if rating not in ALLOWED: errors.append(f"{key}: invalid final_rating {rating!r}")
        for err in e.get("errors",[]):
            if err.get("step") not in expected: errors.append(f"{key}: error references unknown step {err.get('step')}")
    return errors
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data-dir",default="data"); a=ap.parse_args(); d=Path(a.data_dir)
    errs=validate(d/'tasks.json',d/'trajectories.json',d/'evaluations.json')
    if errs:
        print("Validation failed:")
        for x in errs: print("-",x)
        return 1
    print("Validation passed."); return 0
if __name__=="__main__": raise SystemExit(main())
