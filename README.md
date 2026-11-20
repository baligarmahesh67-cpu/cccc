# Basic Crop Recommendation System

A small educational web application. Users enter soil type, growing season,
expected seasonal rainfall and water availability. A Flask backend validates
the inputs and returns a ranked list of crop profiles with a transparent
explanation for each match.

## Technology

- Frontend: HTML, CSS and vanilla JavaScript
- Backend: Python 3 + Flask
- Recommendation logic: editable rule-based scoring (`recommender.py`)
- Hosting: Render (configuration in `render.yaml`)
- Tests: Python `unittest` with a GitHub Actions workflow

## Features

- Responsive form for the four required parameters
- Client-side required-field checks and server-side validation
- JSON API endpoint: `POST /api/recommend`
- Ranked recommendations with a transparent 0-100 rule-based score
- Health endpoint: `GET /health`
- Agricultural reference links shown with the results
- Accessible loading, error and empty states with safe text rendering
- No credentials, paid APIs or database required

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run locally (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Optional syntax checks:

```bash
python -m compileall -q app.py recommender.py crop_data.py tests
node --check static/js/app.js
```

## API example

Request:

```http
POST /api/recommend
Content-Type: application/json
```

```json
{
  "soil_type": "red",
  "season": "Kharif",
  "rainfall_mm": 700,
  "water_availability": "low"
}
```

The response contains `recommendations`, `count` and an agricultural-use
notice. Invalid input, including non-finite rainfall values, returns HTTP 400
with an `error` message. Oversized or unreadable request bodies also return a
JSON error. The browser renders server-provided text with `textContent`, not
`innerHTML`, and handles unreadable API responses.

## Deploy to Render

1. Push this project to the GitHub repository on the `main` branch.
2. In Render, create or update the **basic-crop-recommendation** web service
   from this repository. A Blueprint deployment can read `render.yaml`.
3. Use these settings if configuring the service manually:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Health check path: `/health`
4. Deploy, then open the generated URL.
5. Check `<render-url>/health` returns `{"status":"ok", ...}` and submit the
   form on the home page.

No environment variables or database are required by this version. Render
supplies the `PORT` environment variable; Gunicorn binds to it explicitly.

## Recommendation logic and limits

The rule-based score is composed of:

| Rule | Maximum points |
|---|---:|
| Soil profile match | 35 |
| Season profile match | 25 |
| Rainfall-band proximity | 25 |
| Water-level profile match | 15 |
| **Total** | **100** |

This is a classroom ranking score, not a probability, yield forecast or
scientifically validated measure of farm success. The API returns up to five
results by default; the internal result limit is restricted to 1-10. A crop is
omitted only when neither its soil profile nor its season matches. Profiles and
score weights can be edited in `crop_data.py` and `recommender.py`.

**Important limitation:** the rainfall bands, soil preferences, water-level
preferences and 0-100 scores in `crop_data.py` are prototype screening
assumptions for demonstrating the algorithm. They are not official ICAR
thresholds or a validated agronomic model. The ICAR references support the
inclusion of crops and selected regional context; they do not validate every
soil/water mapping or score used by this demo. Crop suitability depends on
district, agro-climatic zone, soil depth and test results, variety, sowing date,
drainage, actual rainfall distribution, irrigation and local pest/disease
risks. Do not make a real planting decision from this classroom prototype
alone. Confirm local advice with the relevant Krishi Vigyan Kendra (KVK), State
Agricultural University or agriculture department.

## Agricultural references

1. ICAR, *Karnataka* - state profile and important crops:
   <https://www.icar.gov.in/en/node/17269>
2. ICAR, *Kharif Agro-Advisories for Farmers 2025* (PDF, Karnataka section):
   <https://icar.gov.in/sites/default/files/2025-10/ICAR-En-Kharif-Agro-Advisories-for-Farmers-2025.pdf>

The data profiles are a limited educational selection, not a complete national
crop database.

## Project structure

```text
basic_crop_recommendation/
|-- app.py
|-- recommender.py
|-- crop_data.py
|-- requirements.txt
|-- render.yaml
|-- README.md
|-- PROJECT_ARCHITECTURE.md
|-- API_GUIDE.md
|-- MANUAL_TEST_CASES.md
|-- GITHUB_UPLOAD_GUIDE.md
|-- DEPLOYMENT_CHECKLIST.md
|-- .gitignore
|-- templates/
|   `-- index.html
|-- static/
|   |-- css/style.css
|   |-- js/app.js
|   `-- favicon.svg
|-- tests/
|   |-- test_recommender.py
|   `-- test_api.py
`-- .github/
    `-- workflows/tests.yml
```

## Security notes

- No secrets, API keys, passwords or personal data are stored in the repository.
- `.venv/`, `.env` files, caches and compiled Python files are ignored by Git.
- Flask debug mode is disabled; Render runs the app with Gunicorn.
- Responses include basic security headers and API responses are not cached.
- Input is validated on both the client and the server.
