#!/usr/bin/env python3
import argparse, json
from collections import Counter
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--file",default="data/evaluations.json"); a=ap.parse_args()
    evs=json.loads(Path(a.file).read_text()); ratings=Counter(); cats=Counter(); total=failed=0
    for e in evs:
        ratings[e["overall"]["final_rating"]]+=1
        for er in e.get("errors",[]): cats[er["category"]]+=1
        for s in e.get("step_evaluations",[]):
            total+=1
            if not s["intended_effect"]: failed+=1
    print("Computer-Use Evaluation Lab")
    print("="*28)
    print(f"Evaluations: {len(evs)}")
    print(f"Steps reviewed: {total}")
    print(f"Steps without intended effect: {failed}")
    print("\nFinal ratings:")
    for k,v in sorted(ratings.items()): print(f"  {k}: {v}")
    if cats:
        print("\nObserved error categories:")
        for k,v in sorted(cats.items()): print(f"  {k}: {v}")
    return 0
if __name__=="__main__": raise SystemExit(main())
