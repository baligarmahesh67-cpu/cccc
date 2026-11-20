import unittest
from recommender import InputValidationError, recommend_crops


class RecommenderTests(unittest.TestCase):
    def valid(self):
        return {"soil_type": "red", "season": "Kharif", "rainfall_mm": 700, "water_availability": "low"}

    def test_returns_ranked_results(self):
        results = recommend_crops(self.valid())
        self.assertTrue(results)
        scores = [item["match_score"] for item in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_ragi_is_candidate_for_red_soil_kharif(self):
        names = [item["name"] for item in recommend_crops(self.valid())]
        self.assertIn("Finger Millet (Ragi)", names)

    def test_invalid_soil_is_rejected(self):
        data = self.valid()
        data["soil_type"] = "unknown"
        with self.assertRaises(InputValidationError):
            recommend_crops(data)

    def test_invalid_season_is_rejected(self):
        data = self.valid()
        data["season"] = "monsoon"
        with self.assertRaises(InputValidationError):
            recommend_crops(data)

    def test_invalid_water_is_rejected(self):
        data = self.valid()
        data["water_availability"] = "unknown"
        with self.assertRaises(InputValidationError):
            recommend_crops(data)

    def test_rainfall_bounds_are_checked(self):
        for rainfall in (-1, 5001, float("nan"), float("inf"), True):
            data = self.valid()
            data["rainfall_mm"] = rainfall
            with self.subTest(rainfall=rainfall), self.assertRaises(InputValidationError):
                recommend_crops(data)

    def test_safflower_is_candidate_for_black_soil_rabi(self):
        data = {"soil_type": "black", "season": "Rabi", "rainfall_mm": 450, "water_availability": "low"}
        names = [item["name"] for item in recommend_crops(data)]
        self.assertIn("Safflower", names)


if __name__ == "__main__":
    unittest.main()