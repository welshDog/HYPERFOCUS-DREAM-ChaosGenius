import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# ========== CONFIG ==========
PROJECTS_DIR = "test_projects"
SCORECARDS_DIR = "scorecards"
LOGS_DIR = "logs"
BADGES_DIR = "badges"

VERBOSITY = 2  # 1 = minimal, 2 = simple, 3 = full verbose

# ========== REWARD SYSTEM ==========
REWARD_TIERS = [
    (91, "THE Ultimate", 100),
    (76, "Ultra", 50),
    (51, "Super", 25),
    (26, "Good", 10),
    (0, "OK", 1),
]


def detect_projects():
    return [
        f
        for f in os.listdir(PROJECTS_DIR)
        if os.path.isdir(os.path.join(PROJECTS_DIR, f))
    ]


def run_autofix(project_path):
    result = {
        "fixes": 0,
        "errors_fixed": 0,
        "style_score": 0,
        "log": "",
    }

    log = f"### Fix Log for {project_path}\n\n"

    # Run autofix_runner if available
    try:
        cmd = ["python", "tools/autofix_runner.py", project_path]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        output = proc.stdout + "\n" + proc.stderr
        result["log"] = output
        log += output

        # Simulate parsing fix count
        result["fixes"] = output.count("✔")
        result["errors_fixed"] = output.count("❌")
    except Exception as e:
        result["log"] = str(e)
        log += f"\n❌ Error running autofix: {e}"

    # Simulate style score (placeholder)
    result["style_score"] = round(10 - result["errors_fixed"] * 0.5, 2)
    return result, log


def calculate_score(fixes, errors_fixed, style_score):
    score = fixes * 2 + errors_fixed * 3 + style_score * 5
    return min(100, round(score))


def rank_and_reward(score):
    for min_score, rank, reward in REWARD_TIERS:
        if score >= min_score:
            return rank, reward
    return "OK", 1


def save_scorecard(project, data):
    Path(SCORECARDS_DIR).mkdir(exist_ok=True)
    Path(LOGS_DIR).mkdir(exist_ok=True)

    scorecard_path = os.path.join(SCORECARDS_DIR, f"{project}.json")
    with open(scorecard_path, "w") as f:
        json.dump(data, f, indent=4)

    log_path = os.path.join(LOGS_DIR, f"fix_log_{project}.md")
    with open(log_path, "w") as f:
        f.write(data.get("log", ""))


def main():
    print("🧪🛠️ BROSKI FIX LAB INITIATED!")
    projects = detect_projects()
    if not projects:
        print("⚠️ No test projects found.")
        return

    for project in projects:
        print(f"\n🔍 Analyzing project: {project}")
        path = os.path.join(PROJECTS_DIR, project)

        result, raw_log = run_autofix(path)
        score = calculate_score(
            result["fixes"], result["errors_fixed"], result["style_score"]
        )
        rank, reward = rank_and_reward(score)

        data = {
            "project": project,
            "score": score,
            "rank": rank,
            "broski_bucks": reward,
            "fixes": result["fixes"],
            "errors_fixed": result["errors_fixed"],
            "style_score": result["style_score"],
            "badge": f"{BADGES_DIR}/{rank}.svg",
            "log_file": f"{LOGS_DIR}/fix_log_{project}.md",
            "log": raw_log,
        }

        save_scorecard(project, data)

        print(f"🏆 RANK: {rank} | 💰 BROski$: +{reward} | 🔧 Score: {score}/100")


if __name__ == "__main__":
    main()
