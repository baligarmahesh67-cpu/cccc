import json
import unittest

from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def valid_payload(self):
        return {
            "soil_type": "red",
            "season": "Kharif",
            "rainfall_mm": 700,
            "water_availability": "low",
        }

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        body = response.get_data(as_text=True)
        self.assertIn("CropWise", body)
        self.assertIn('id="recommend-form"', body)
        self.assertIn('id="soil_type"', body)
        self.assertIn('id="season"', body)
        self.assertIn('id="rainfall_mm"', body)
        self.assertIn('id="water_availability"', body)
        self.assertIn("/static/css/style.css", body)
        self.assertIn("/static/js/app.js", body)
        self.assertIn("/static/favicon.svg", body)
        self.assertIn("not probabilities", body)
        self.assertNotIn("\ufffd", body)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.get_json(), {
            "status": "ok",
            "service": "basic-crop-recommendation",
        })

    def test_static_css_is_served(self):
        response = self.client.get("/static/css/style.css")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "text/css")
            self.assertIn(b":root", response.data)
            self.assertIn(b"@media", response.data)
        finally:
            response.close()

    def test_css_matches_the_template_layout(self):
        response = self.client.get("/static/css/style.css")
        try:
            self.assertEqual(response.status_code, 200)
            css = response.get_data(as_text=True)
            for selector in (".form-panel", ".results-panel", ".workspace", ".hero-art"):
                self.assertIn(selector, css)
            self.assertIn("@media(max-width:850px)", css)
            self.assertIn("@media(max-width:520px)", css)
        finally:
            response.close()

    def test_static_javascript_is_served(self):
        response = self.client.get("/static/js/app.js")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn("javascript", response.mimetype)
            self.assertIn(b"/api/recommend", response.data)
            self.assertIn(b"reportValidity", response.data)
        finally:
            response.close()

    def test_favicon_is_served(self):
        response = self.client.get("/static/favicon.svg")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn("svg", response.mimetype)
            self.assertIn(b"<svg", response.data)
        finally:
            response.close()

    def test_recommendation_endpoint(self):
        response = self.client.post("/api/recommend", json=self.valid_payload())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        body = response.get_json()
        self.assertGreater(body["count"], 0)
        self.assertEqual(body["count"], len(body["recommendations"]))
        self.assertIn("notice", body)
        first = body["recommendations"][0]
        self.assertIn("match_score", first)
        self.assertIn("reasons", first)
        self.assertIn("source", first)
        self.assertLessEqual(body["count"], 5)

    def test_recommendation_order_is_descending(self):
        response = self.client.post("/api/recommend", json=self.valid_payload())
        scores = [item["match_score"] for item in response.get_json()["recommendations"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_invalid_input_returns_400(self):
        response = self.client.post("/api/recommend", json={"soil_type": "bad"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_each_invalid_field_returns_400(self):
        cases = {
            "soil_type": "unknown",
            "season": "monsoon",
            "water_availability": "unknown",
            "rainfall_mm": -1,
        }
        for field, value in cases.items():
            with self.subTest(field=field):
                payload = self.valid_payload()
                payload[field] = value
                response = self.client.post("/api/recommend", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_missing_fields_return_400(self):
        for field in ("soil_type", "season", "rainfall_mm", "water_availability"):
            with self.subTest(field=field):
                payload = self.valid_payload()
                del payload[field]
                response = self.client.post("/api/recommend", json=payload)
                self.assertEqual(response.status_code, 400)

    def test_rainfall_above_limit_returns_400(self):
        payload = self.valid_payload()
        payload["rainfall_mm"] = 5001
        response = self.client.post("/api/recommend", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_non_finite_rainfall_returns_400(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                payload = self.valid_payload()
                payload["rainfall_mm"] = value
                # allow_nan keeps the JSON encoder from raising before the
                # request reaches the application.
                response = self.client.post(
                    "/api/recommend",
                    data=json.dumps(payload, allow_nan=True),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_empty_and_non_object_json_return_400(self):
        for payload in ({}, [], None, "red", 7, True):
            with self.subTest(payload=payload):
                response = self.client.post("/api/recommend", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_empty_body_returns_400(self):
        response = self.client.post("/api/recommend", data=b"", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_returns_400(self):
        response = self.client.post(
            "/api/recommend",
            data='{"soil_type":',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_non_json_content_type_returns_400(self):
        response = self.client.post(
            "/api/recommend",
            data="soil_type=red",
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_oversized_request_returns_json_413(self):
        response = self.client.post(
            "/api/recommend",
            data="x" * (17 * 1024),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 413)
        self.assertIn("error", response.get_json())

    def test_unknown_api_path_returns_404(self):
        response = self.client.get("/api/unknown")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_unknown_page_returns_404(self):
        response = self.client.get("/missing-page")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "text/html")

    def test_wrong_method_returns_405(self):
        response = self.client.get("/api/recommend")
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.get_json())

        response = self.client.post("/health")
        self.assertEqual(response.status_code, 405)

    def test_security_headers_are_present(self):
        response = self.client.get("/health")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
        self.assertIn("default-src 'self'", response.headers.get("Content-Security-Policy", ""))
        self.assertIn("geolocation=()", response.headers.get("Permissions-Policy", ""))

    def test_api_responses_are_not_cached(self):
        response = self.client.post("/api/recommend", json=self.valid_payload())
        self.assertEqual(response.headers.get("Cache-Control"), "no-store")

    def test_api_rejects_unknown_extra_fields_gracefully(self):
        payload = self.valid_payload()
        payload["administrator"] = True
        payload["debug"] = "true"
        response = self.client.post("/api/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("debug", response.get_json())


if __name__ == "__main__":
    unittest.main()
