# Solace — financial capability prototype

A working prototype of **Solace**, a financial capability platform for
18–25 year-olds, built around five layers:

1. **Detect** — a short questionnaire (standing in for an open-banking
   connection) builds a profile of the user's real financial situation.
2. **Learn** — short lessons, reordered per user so the ones most relevant
   to their profile come first.
3. **Practice** — scenario-based decisions with branching feedback, built
   from the same profile.
4. **Reward** — daily check-ins, a streak counter, points, and a
   redeemable cash top-up once a points threshold is hit.
5. **Social** — a lightweight streak leaderboard.

Everything is a real, working Flask app — no real bank connection and no
real money move, but every button does something (session-backed state,
real branching logic, real point totals).

## Project structure

```
solace_app/
├── app.py                 # Flask routes and session logic
├── data.py                # Lessons, scenarios, questionnaire, rules
├── requirements.txt
├── Procfile                # for Heroku / Railway-style platforms
├── render.yaml              # optional one-click Render blueprint
├── runtime.txt               # pinned Python version
├── .env.example
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── base.html
    ├── index.html
    ├── detect.html
    ├── detect_result.html
    ├── learn.html
    ├── lesson_detail.html
    ├── practice.html
    ├── scenario_detail.html
    ├── reward.html
    └── social.html
```

## Running it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional — sets a local SECRET_KEY
python app.py
```

Then open **http://127.0.0.1:5000**.

There's a **Reset demo** button in the nav bar on every page — it clears
your session so you can re-run the whole flow from scratch, which is
handy when presenting it live.

## Deploying it

The app is a standard Flask app served by `gunicorn`, so it runs on any
platform that supports Python. A `Procfile` and `runtime.txt` are
included for Heroku/Railway-style platforms, and a `render.yaml` is
included for a one-click [Render](https://render.com) deploy.

### Render (easiest, free tier available)
1. Push/upload this repo to GitHub.
2. In Render, choose **New → Blueprint** and point it at the repo —
   it will read `render.yaml` automatically. Or choose **New → Web
   Service**, connect the repo, and set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Set a `SECRET_KEY` environment variable to a random string (Render's
   blueprint does this for you automatically).

### Railway / Heroku
1. Connect the GitHub repo.
2. Both platforms detect the `Procfile` automatically
   (`web: gunicorn app:app`).
3. Set a `SECRET_KEY` config var / environment variable.

### Anything else (PythonAnywhere, a VPS, Docker, etc.)
Install `requirements.txt` and run the app with any WSGI server pointed
at `app:app` (e.g. `gunicorn app:app`), setting `SECRET_KEY` as an
environment variable.

> Note: GitHub itself only hosts static files (GitHub Pages), so this
> Flask app needs a platform like the ones above to actually run —
> GitHub is just where the code lives and where a host like Render or
> Railway pulls it from.

## Notes on the demo data

All lessons, scenarios, and the leaderboard live in `data.py` as plain
Python lists/dicts — no database. State per visitor (profile tags,
completed lessons/scenarios, points, streak) lives in the Flask
session, so it resets whenever a session/cookie is cleared, and isn't
shared between visitors. That's intentional for a demo; a real build
would swap this for a proper database and real open-banking data.
