import math
import unittest

from recommender import InputValidationError, recommend_crops


class RecommenderTests(unittest.TestCase):
    def valid(self):
        return {
            "soil_type": "red",
            "season": "Kharif",
            "rainfall_mm": 700,
            "water_availability": "low",
        }

    def test_returns_ranked_results(self):
        results = recommend_crops(self.valid())
        self.assertTrue(results)
        scores = [item["match_score"] for item in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertLessEqual(len(results), 5)

    def test_ragi_is_candidate_for_red_soil_kharif(self):
        names = [item["name"] for item in recommend_crops(self.valid())]
        self.assertIn("Finger Millet (Ragi)", names)

    def test_result_shape_and_explanations(self):
        result = recommend_crops(self.valid())[0]
        expected = {
            "name",
            "match_score",
            "description",
            "reasons",
            "evidence",
            "source",
            "prototype_rainfall_band_mm",
        }
        self.assertEqual(set(result), expected)
        self.assertIsInstance(result["match_score"], int)
        self.assertGreaterEqual(result["match_score"], 0)
        self.assertLessEqual(result["match_score"], 100)
        self.assertTrue(result["reasons"])
        self.assertTrue(result["source"].startswith("https://"))
        self.assertEqual(len(result["prototype_rainfall_band_mm"]), 2)

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
        for rainfall in (-1, 5001, float("nan"), float("inf"), float("-inf"), True):
            with self.subTest(rainfall=rainfall):
                data = self.valid()
                data["rainfall_mm"] = rainfall
                with self.assertRaises(InputValidationError):
                    recommend_crops(data)

    def test_rainfall_boundary_values_are_accepted(self):
        for rainfall in (0, 5000, "700", 700.5):
            with self.subTest(rainfall=rainfall):
                data = self.valid()
                data["rainfall_mm"] = rainfall
                self.assertTrue(recommend_crops(data))

    def test_missing_and_unusable_rainfall_is_rejected(self):
        for rainfall in (None, "", "  ", "not-a-number", [], {}, object()):
            with self.subTest(rainfall=rainfall):
                data = self.valid()
                data["rainfall_mm"] = rainfall
                with self.assertRaises(InputValidationError):
                    recommend_crops(data)

    def test_non_finite_string_rainfall_is_rejected(self):
        for rainfall in ("nan", "inf", "-Infinity", "1e309"):
            with self.subTest(rainfall=rainfall):
                data = self.valid()
                data["rainfall_mm"] = rainfall
                with self.assertRaises(InputValidationError):
                    recommend_crops(data)

    def test_missing_required_fields_are_rejected(self):
        for field in ("soil_type", "season", "rainfall_mm", "water_availability"):
            with self.subTest(field=field):
                data = self.valid()
                del data[field]
                with self.assertRaises(InputValidationError):
                    recommend_crops(data)

    def test_empty_and_wrong_payload_types_are_rejected(self):
        for payload in ({}, [], None, "red", 7):
            with self.subTest(payload=payload):
                with self.assertRaises(InputValidationError):
                    recommend_crops(payload)

    def test_invalid_choice_types_are_rejected(self):
        for field in ("soil_type", "season", "water_availability"):
            for value in (None, "", "   ", 1, True, [], {}):
                with self.subTest(field=field, value=value):
                    data = self.valid()
                    data[field] = value
                    with self.assertRaises(InputValidationError):
                        recommend_crops(data)

    def test_case_and_whitespace_insensitive_choices_are_accepted(self):
        results = recommend_crops({
            "soil_type": "  RED ",
            "season": " kharif ",
            "rainfall_mm": "700",
            "water_availability": " LOW ",
        })
        self.assertTrue(results)

    def test_safflower_is_candidate_for_black_soil_rabi(self):
        data = {
            "soil_type": "black",
            "season": "Rabi",
            "rainfall_mm": 450,
            "water_availability": "low",
        }
        names = [item["name"] for item in recommend_crops(data)]
        self.assertIn("Safflower", names)

    def test_invalid_result_limit_is_rejected(self):
        for value in (0, 11, -1, 1.5, True, "5", None):
            with self.subTest(value=value):
                with self.assertRaises(InputValidationError):
                    recommend_crops(self.valid(), limit=value)

    def test_limit_is_respected(self):
        for limit in (1, 3, 10):
            with self.subTest(limit=limit):
                results = recommend_crops(self.valid(), limit=limit)
                self.assertLessEqual(len(results), limit)

    def test_scores_are_finite_and_ranked(self):
        for soil in ("red", "black", "alluvial", "clay", "sandy", "loamy", "laterite"):
            for season in ("Kharif", "Rabi", "Summer"):
                with self.subTest(soil=soil, season=season):
                    results = recommend_crops({
                        "soil_type": soil,
                        "season": season,
                        "rainfall_mm": 700,
                        "water_availability": "moderate",
                    })
                    self.assertTrue(results)
                    scores = [item["match_score"] for item in results]
                    self.assertTrue(all(math.isfinite(score) for score in scores))
                    self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
