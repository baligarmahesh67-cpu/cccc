# Manual Test Cases

Use the running app at `http://127.0.0.1:5000`. These examples are functional checks, not agronomic advice.

| Test | Soil | Season | Seasonal rainfall (mm) | Water | Expected behavior |
|---|---|---:|---:|---|---|
| 1 | Red | Kharif | 700 | Low | Ranked list includes Finger Millet (Ragi) |
| 2 | Black | Rabi | 450 | Low | Ranked list includes Safflower |
| 3 | Loamy | Kharif | 900 | Moderate | Returns a ranked list with explanations |
| 4 | Red | Kharif | -5 | Low | Browser blocks invalid negative rainfall |
| 5 | Red | Kharif | 5001 | Low | Browser blocks rainfall above 5000 mm |
| 6 | Not selected | Kharif | 700 | Low | Browser asks for required soil type |
| 7 | Red | Not selected | 700 | Low | Browser asks for required season |
| 8 | Red | Kharif | blank | Low | Browser asks for rainfall |
| 9 | Red | Kharif | 700 | Not selected | Browser asks for water availability |

## API check

Send a JSON `POST` request to `/api/recommend` with the four values. A valid request should return HTTP 200. Invalid or missing values should return HTTP 400. `GET /health` should return HTTP 200 with `status: ok`.
