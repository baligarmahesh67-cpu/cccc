# API Guide

Base URL when running locally: `http://127.0.0.1:5000`

## `GET /`

Returns the HTML application page.

## `GET /health`

Returns service health.

Example response:

```json
{
  "status": "ok",
  "service": "basic-crop-recommendation"
}
```

## `POST /api/recommend`

Content type: `application/json`

Request body:

```json
{
  "soil_type": "red",
  "season": "Kharif",
  "rainfall_mm": 700,
  "water_availability": "low"
}
```

Allowed soil values: `red`, `black`, `alluvial`, `clay`, `sandy`, `loamy`,
`laterite`.

Allowed seasons: `Kharif`, `Rabi`, `Summer`.

Allowed water values: `low`, `moderate`, `high`.

Rainfall must be a finite number from 0 to 5000 mm.

Choice values are matched without regard to letter case or surrounding spaces.
Unknown extra fields are ignored.

Success response (HTTP 200) includes:

- `recommendations`: ranked crop profiles, each with `name`, `match_score`,
  `description`, `reasons`, `evidence`, `source`, and
  `prototype_rainfall_band_mm`.
- `count`: number of returned crops (maximum 5 by default).
- `notice`: educational-use disclaimer.

Common error responses:

- `400`: malformed JSON, a non-object JSON body, or an invalid/missing field.
- `404`: unknown API path.
- `405`: unsupported HTTP method.
- `413`: request body larger than 16 KB.

All API errors are JSON objects with an `error` field.

## Example using curl

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"soil_type":"red","season":"Kharif","rainfall_mm":700,"water_availability":"low"}'
```

## Example error using curl

```bash
curl -i -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"soil_type":"red","season":"monsoon","rainfall_mm":700,"water_availability":"low"}'
```

Expected: HTTP 400 with a JSON `error` message.

The returned `match_score` is an illustrative rule score, not a probability,
yield forecast or official agronomic threshold.
