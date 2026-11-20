# Project Architecture

## Goal

A classroom demonstrator that accepts four inputs from the project statement: soil type, growing season, expected seasonal rainfall (mm), and water availability. It returns up to five ranked crop profiles and explains which prototype rules matched.

## Architecture

```text
Browser
  |
  | HTML form + CSS + JavaScript
  | POST /api/recommend (JSON)
  v
Python Flask application (app.py)
  |
  v
Input validation + rule ranking (recommender.py)
  |
  v
Crop profiles and reference notes (crop_data.py)
  |
  v
JSON response -> browser results cards
```

## Frontend

- `templates/index.html`: form, page layout, references, and accessible result containers.
- `static/css/style.css`: responsive presentation for desktop and mobile.
- `static/js/app.js`: form submission, loading/error states, safe result rendering, and reset behavior.

## Backend

- `app.py`: serves the page, health endpoint, JSON API, request-size limit, and basic security headers.
- `recommender.py`: validates user input and computes a transparent rule-based ranking.
- `crop_data.py`: editable crop profiles, prototype bands and source notes.

## Scoring design

| Rule | Maximum points |
|---|---:|
| Soil profile match | 35 |
| Season profile match | 25 |
| Rainfall band proximity | 25 |
| Water availability profile match | 15 |
| **Total** | **100** |

The output is a rule score, not a statistical probability, yield prediction, or guarantee of suitability. Crops with neither a soil nor a season profile match are excluded. The top five remaining results are returned.

## Storage

No database is used. Inputs are submitted for a calculation and are not stored by this application. No user account or login is needed for this classroom version.

## External dependencies

The browser uses native HTML, CSS and JavaScript. The server uses Flask; Gunicorn runs the app on Render. No paid API or API secret is needed.

## Production-readiness boundary

This is a small academic prototype, not a farm advisory service. Before using it for an actual planting decision, extend the profiles using district-level, agro-climatic-zone, soil-test, crop-variety and current-season information verified by a Krishi Vigyan Kendra or State Agricultural University.
