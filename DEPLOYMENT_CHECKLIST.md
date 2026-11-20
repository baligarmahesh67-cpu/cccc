# GitHub + Render Release Checklist

## Before GitHub

- [ ] Create and activate `.venv`; install `requirements.txt`.
- [ ] Run `python -m unittest discover -s tests -v` with zero failures and
      zero unexplained skips.
- [ ] Run `python -m compileall -q app.py recommender.py crop_data.py tests`.
- [ ] Run `node --check static/js/app.js` (or report if Node.js is unavailable).
- [ ] Run the site locally and test valid and invalid form inputs.
- [ ] Confirm no `.env`, passwords, API tokens or personal data are committed.
- [ ] Confirm crop thresholds have been reviewed by a local agriculture subject
      expert before any real-farmer use.
- [ ] Add team member names / guide / institution details only if required by
      the assignment.

## GitHub

- [ ] Confirm the remote is the intended repository and the branch is `main`.
- [ ] Confirm `app.py`, `requirements.txt`, `render.yaml`, `templates/`,
      `static/` and `tests/` are in the repository root.
- [ ] Push without force and confirm the remote SHA matches local `HEAD`.
- [ ] Confirm the GitHub Actions workflow completes with conclusion `SUCCESS`.

## Render

- [ ] Create or update the **basic-crop-recommendation** web service from the
      existing repository. Do not create a duplicate service.
- [ ] Build command: `pip install -r requirements.txt`.
- [ ] Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`.
- [ ] Health check path: `/health`.
- [ ] Confirm the deployed commit matches the tested GitHub commit.
- [ ] After deployment, verify `/health` responds with HTTP 200.
- [ ] Test the complete recommendation form on the public URL, including
      invalid values.
- [ ] Keep the repository connected for later automatic deploys from `main`.

## Current verification status

Update only after the check has actually been performed:

- [ ] Python source compilation
- [ ] JavaScript syntax check
- [ ] Recommendation unit tests
- [ ] Flask API tests
- [ ] Local application runtime test
- [ ] GitHub Actions workflow
- [ ] Live Render deployment test
- [ ] Mobile / responsive browser test
- [ ] Agricultural expert review

Do not mark a check complete until it has actually been performed.
