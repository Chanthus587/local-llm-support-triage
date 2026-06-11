import unittest

from support_triage.services.triage import normalize_result, rules_fallback


class TriageTests(unittest.TestCase):
    def test_rules_fallback_detects_billing_priority(self) -> None:
        result = rules_fallback(
            "Payment failed but card was charged",
            "This is urgent because our renewal is blocked.",
        )

        self.assertEqual(result.category, "billing")
        self.assertEqual(result.priority, "high")
        self.assertEqual(result.assigned_team, "Billing Operations")
        self.assertEqual(result.model_name, "rules-fallback")

    def test_normalize_result_bounds_confidence_and_category(self) -> None:
        result = normalize_result(
            {
                "category": "unknown",
                "priority": "critical",
                "sentiment": "angry",
                "confidence": 7,
                "summary": "Customer has an issue.",
                "recommended_action": "Review manually.",
            },
            subject="Problem",
            body="Help",
            model_name="test-model",
        )

        self.assertEqual(result.category, "general")
        self.assertEqual(result.priority, "medium")
        self.assertEqual(result.sentiment, "neutral")
        self.assertEqual(result.confidence, 1.0)


if __name__ == "__main__":
    unittest.main()
