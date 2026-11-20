# GitHub + Render release checklist

## Before GitHub
- [ ] Run `python -m unittest discover -s tests -v`. The current offline build check reports 13 passing recommender tests and 8 Flask API tests skipped because Flask could not be installed in this workspace; GitHub Actions is configured to install `requirements.txt` and run the full suite.
- [ ] Run the site locally and test each soil / season / rainfall / water input.
- [ ] Confirm no `.env`, passwords, API tokens or personal data are committed.
- [ ] Confirm crop thresholds have been reviewed by a local agriculture subject expert before any real-farmer use.
- [ ] Add team member names / guide / institution details only if required by the assignment.

## GitHub
- [ ] Create a new repository (public or private as appropriate).
- [ ] Upload the contents of this folder, not the ZIP file alone.
- [ ] Confirm `app.py`, `requirements.txt`, `render.yaml`, `templates/`, and `static/` are in the repository root.

## Render
- [ ] Create a Web Service or Blueprint from the GitHub repository.
- [ ] Build command: `pip install -r requirements.txt`.
- [ ] Start command: `gunicorn app:app`.
- [ ] After deployment, verify `/health` responds with HTTP 200.
- [ ] Test the complete recommendation form on the public URL, including invalid values.
- [ ] Keep the repository connected for later automatic deploys from the selected branch.

## Current verification status
- [x] Python source compilation
- [x] JavaScript syntax check
- [x] Recommendation tests (13 passed)
- [ ] Flask API tests (8 skipped locally; run in GitHub Actions)
- [ ] Application runtime test
- [ ] Automated unit/API tests
- [ ] Real-user / mobile-browser test
- [ ] Live Render deployment test
- [ ] Agricultural expert review

Do not mark the last four checks complete until they have actually been performed.
