"""Score the message checker on eval/messages.json (synthetic, written blind to the checker's code).

Run: .venv/Scripts/python -m eval.messages_eval
"""
import json
import re
import sys
import pathlib

from backend.check import check_text

HERE = pathlib.Path(__file__).parent


def unmask(text: str) -> str:
    """The synthetic set masks numbers (97XXXX4410); real messages carry digits, so fill the mask in."""
    return re.sub(r"(?<=[\d-])[Xx]+(?=[\d-])", lambda m: "5" * len(m.group()), text)


def main(name="messages"):
    rows = json.loads((HERE / f"{name}.json").read_text(encoding="utf-8"))
    tp = fp = fn = tn = 0
    misses, false_alarms = [], []
    for r in rows:
        v = check_text(unmask(r["text"]))["verdict"]
        flagged = v != "safe"  # "Be careful" or "Scam" both warn the user
        if r["label"] == "scam":
            tp += flagged; fn += not flagged
            if not flagged: misses.append(r)
        else:
            fp += flagged; tn += not flagged
            if flagged: false_alarms.append((v, r))
    out = {"messages": len(rows), "scams": tp + fn, "genuine": tn + fp, "caught": tp, "missed": fn,
           "false_alarms": fp, "precision": round(tp / max(1, tp + fp), 3), "recall": round(tp / max(1, tp + fn), 3)}
    (HERE / f"{name}_results.json").write_text(json.dumps({**out,
        "missed_kinds": [m["kind"] for m in misses], "false_alarm_kinds": [f"{r['kind']} ({v})" for v, r in false_alarms]}, indent=2))
    print(json.dumps(out))
    for m in misses: print("MISS", m["kind"], "|", m["text"][:110])
    for v, r in false_alarms: print("FALSE", v, r["kind"], "|", r["text"][:110])


if __name__ == "__main__":
    main(*sys.argv[1:])
