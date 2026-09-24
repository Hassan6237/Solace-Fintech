"""Solace — working prototype.

A Flask app demonstrating the five-layer flow (Detect, Learn, Practice,
Reward, Social) end to end using session-based state. No real accounts,
no real bank connections, no real payments — everything here is a
working stand-in built for demoing the product idea.

Local run:
    python app.py
then open http://127.0.0.1:5000

Production (e.g. behind gunicorn on Render/Railway/Heroku):
    gunicorn app:app
"""
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

import data

load_dotenv()  # reads a local .env file if present; no-op in production

app = Flask(__name__)
# In production, set a real SECRET_KEY environment variable — this fallback
# is fine for local demoing only.
app.secret_key = os.environ.get("SECRET_KEY", "solace-prototype-demo-key")


# ---------------------------------------------------------------- helpers

def get_state():
    """Ensure session has all the fields the prototype needs, and return it."""
    session.setdefault("answers", {})
    session.setdefault("tags", [])
    session.setdefault("completed_lessons", [])
    session.setdefault("completed_scenarios", [])
    session.setdefault("points", 0)
    session.setdefault("streak", 0)
    session.setdefault("last_checkin", None)
    session.setdefault("redeemed_topups", 0)
    return session


def add_points(amount):
    session["points"] = session.get("points", 0) + amount
    session.modified = True


# ------------------------------------------------------------------ views

@app.route("/")
def index():
    state = get_state()
    onboarded = bool(state["answers"])
    return render_template(
        "index.html",
        onboarded=onboarded,
        tags=state["tags"],
        points=state["points"],
        streak=state["streak"],
        lessons_done=len(state["completed_lessons"]),
        lessons_total=len(data.LESSONS),
        scenarios_done=len(state["completed_scenarios"]),
        scenarios_total=len(data.SCENARIOS),
    )


@app.route("/detect", methods=["GET", "POST"])
def detect():
    state = get_state()
    if request.method == "POST":
        answers = {}
        for q in data.QUESTIONNAIRE:
            val = request.form.get(q["id"])
            if val:
                answers[q["id"]] = val
        state["answers"] = answers
        state["tags"] = data.tags_for_answers(answers)
        session.modified = True
        return redirect(url_for("detect_result"))
    return render_template("detect.html", questionnaire=data.QUESTIONNAIRE)


@app.route("/detect/result")
def detect_result():
    state = get_state()
    if not state["answers"]:
        return redirect(url_for("detect"))
    top_lessons = data.relevant(data.LESSONS, state["tags"])[:3]
    top_scenarios = data.relevant(data.SCENARIOS, state["tags"])[:2]
    return render_template(
        "detect_result.html",
        tags=state["tags"],
        top_lessons=top_lessons,
        top_scenarios=top_scenarios,
    )


@app.route("/learn")
def learn():
    state = get_state()
    lessons = data.relevant(data.LESSONS, state["tags"])
    return render_template(
        "learn.html",
        lessons=lessons,
        completed=state["completed_lessons"],
        tags=state["tags"],
    )


@app.route("/learn/<lesson_id>")
def lesson_detail(lesson_id):
    state = get_state()
    lesson = next((l for l in data.LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return redirect(url_for("learn"))
    matched = bool(set(lesson.get("tags", [])) & set(state["tags"]))
    return render_template(
        "lesson_detail.html",
        lesson=lesson,
        matched=matched,
        completed=lesson_id in state["completed_lessons"],
    )


@app.route("/learn/<lesson_id>/complete", methods=["POST"])
def complete_lesson(lesson_id):
    state = get_state()
    earned = 0
    if lesson_id not in state["completed_lessons"]:
        state["completed_lessons"].append(lesson_id)
        add_points(data.POINTS_PER_LESSON)
        earned = data.POINTS_PER_LESSON
        session.modified = True
    return redirect(url_for("lesson_detail", lesson_id=lesson_id, earned=earned or None))


@app.route("/practice")
def practice():
    state = get_state()
    scenarios = data.relevant(data.SCENARIOS, state["tags"])
    return render_template(
        "practice.html",
        scenarios=scenarios,
        completed=state["completed_scenarios"],
    )


@app.route("/practice/<scenario_id>", methods=["GET", "POST"])
def scenario_detail(scenario_id):
    state = get_state()
    scenario = next((s for s in data.SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return redirect(url_for("practice"))

    chosen = None
    earned = 0
    if request.method == "POST":
        choice_id = request.form.get("choice")
        chosen = next((o for o in scenario["options"] if o["id"] == choice_id), None)
        if chosen and scenario_id not in state["completed_scenarios"]:
            state["completed_scenarios"].append(scenario_id)
            add_points(data.POINTS_PER_SCENARIO)
            earned = data.POINTS_PER_SCENARIO
            session.modified = True

    return render_template("scenario_detail.html", scenario=scenario, chosen=chosen, earned=earned)


@app.route("/reward")
def reward():
    state = get_state()
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    checked_in_today = state["last_checkin"] == today
    can_topup = state["points"] >= data.TOPUP_THRESHOLD
    progress_pct = min(100, int(state["points"] / data.TOPUP_THRESHOLD * 100))
    return render_template(
        "reward.html",
        points=state["points"],
        streak=state["streak"],
        checked_in_today=checked_in_today,
        can_topup=can_topup,
        progress_pct=progress_pct,
        threshold=data.TOPUP_THRESHOLD,
        topup_amount=data.TOPUP_AMOUNT_GBP,
        redeemed=state["redeemed_topups"],
    )


@app.route("/reward/checkin", methods=["POST"])
def checkin():
    state = get_state()
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    earned = None
    if state["last_checkin"] != today:
        if state["last_checkin"] == yesterday:
            state["streak"] = state.get("streak", 0) + 1
        else:
            state["streak"] = 1
        state["last_checkin"] = today
        add_points(data.CHECKIN_POINTS)
        earned = data.CHECKIN_POINTS
        session.modified = True
    return redirect(url_for("reward", earned=earned))


@app.route("/reward/topup", methods=["POST"])
def topup():
    state = get_state()
    if state["points"] >= data.TOPUP_THRESHOLD:
        state["points"] -= data.TOPUP_THRESHOLD
        state["redeemed_topups"] = state.get("redeemed_topups", 0) + 1
        session.modified = True
    return redirect(url_for("reward"))


@app.route("/social")
def social():
    state = get_state()
    board = [dict(b) for b in data.LEADERBOARD]
    board.append({"name": "You", "streak": state["streak"], "you": True})
    board.sort(key=lambda b: b["streak"], reverse=True)
    return render_template("social.html", board=board, streak=state["streak"])


@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
