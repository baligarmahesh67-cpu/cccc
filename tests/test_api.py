import unittest
from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CropWise", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_recommendation_endpoint(self):
        response = self.client.post("/api/recommend", json={
            "soil_type": "red", "season": "Kharif", "rainfall_mm": 700, "water_availability": "low"
        })
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.get_json()["count"], 0)

    def test_invalid_input_returns_400(self):
        response = self.client.post("/api/recommend", json={"soil_type": "bad"})
        self.assertEqual(response.status_code, 400)

    def test_unknown_api_path_returns_404(self):
        response = self.client.get("/api/unknown")
        self.assertEqual(response.status_code, 404)

    def test_wrong_method_returns_405(self):
        response = self.client.get("/api/recommend")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()