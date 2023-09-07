"""
Unit tests for the BoredAPI app
"""

import unittest
from unittest.mock import Mock, patch

from main import BoredAPIWrapper, ActivityDatabase


class TestBoredAPIWrapper(unittest.TestCase):

    def setUp(self):
        self.api = BoredAPIWrapper()

    @patch("main.requests.get")
    def test_get_mock_activity(self, mock_get):
        """
        This test simulates API responses using mocks and checks if the returned activity
        matches the expected criteria based on filters.

        Args:
            mock_get (unittest.mock.Mock): The mocked requests.get function.
        """

        # Create a mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "activity": "Learn Express.js",
            "type": "education",
            "participants": 1,
            "price": 0.1,
            "accessibility": 0.1
        }

        # Assign the mock response to the mock_get function
        mock_get.return_value = mock_response

        # Test with no filters
        activity = self.api.get_random_activity()
        self.assertIsNotNone(activity)

        # Test with filters
        activity = self.api.get_random_activity(activity_type="education", participants=1, price_min=0.1, price_max=30,
                                           accessibility_min=0.1, accessibility_max=0.5)
        self.assertIsNotNone(activity)
        self.assertEqual(activity["type"], "education")
        self.assertEqual(activity["participants"], 1)
        self.assertTrue(0.1 <= activity["price"] <= 30)
        self.assertTrue(0.1 <= activity["accessibility"] <= 0.5)

    def test_keys_activity(self):
        """
        This test checks if the get_random_activity method returns a dictionary and if the
        returned activity has the expected keys.
        """

        # Test if get_random_activity returns a dictionary
        activity = self.api.get_random_activity()
        self.assertIsInstance(activity, dict)

        # Test if the returned activity has expected keys
        expected_keys = ["activity", "type", "participants", "price", "accessibility"]
        for key in expected_keys:
            self.assertIn(key, activity)


class TestActivityDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database for testing
        self.db = ActivityDatabase(":memory:")

    def test_save_activity(self):
        """
        This test inserts a test activity into the database and checks if it was saved
        correctly.
        """

        activity = {
            "activity": "Test Activity",
            "type": "test",
            "participants": 2,
            "price": 0.5,
            "accessibility": 0.3
        }

        self.db.save_activity(activity)

        # Check if the activity was saved
        latest_activities = self.db.get_latest_activities()
        self.assertEqual(len(latest_activities), 1)
        saved_activity = latest_activities[0]
        self.assertEqual(saved_activity[1], "Test Activity")

    def test_get_latest_activities(self):
        """
        This test inserts additional test activities into the database, retrieves a limited
        number of the latest activities, and checks if they match the expected results.
        """

        # Insert test data into the database
        test_activities = [
            {
                "activity": "Test Activity 1",
                "type": "test",
                "participants": 1,
                "price": 0.1,
                "accessibility": 0.2
            },
            {
                "activity": "Test Activity 2",
                "type": "test",
                "participants": 2,
                "price": 0.2,
                "accessibility": 0.3
            }
        ]

        for activity in test_activities:
            self.db.save_activity(activity)

        # Retrieve the latest activities
        latest_activities = self.db.get_latest_activities()
        self.assertEqual(len(latest_activities), 2)
        self.assertEqual(latest_activities[0][1], "Test Activity 2")
        self.assertEqual(latest_activities[1][1], "Test Activity 1")

    def test_get_latest_activities_limit(self):
        # Insert more test data into the database
        test_activities = [
            {
                "activity": "Test Activity 3",
                "type": "test",
                "participants": 1,
                "price": 0.1,
                "accessibility": 0.2
            },
            {
                "activity": "Test Activity 4",
                "type": "test",
                "participants": 2,
                "price": 0.2,
                "accessibility": 0.3
            },
            {
                "activity": "Test Activity 5",
                "type": "test",
                "participants": 3,
                "price": 0.3,
                "accessibility": 0.4
            }
        ]

        for activity in test_activities:
            self.db.save_activity(activity)

        # Retrieve the latest 2 activities
        latest_activities = self.db.get_latest_activities(limit=2)
        self.assertEqual(len(latest_activities), 2)
        self.assertEqual(latest_activities[0][1], "Test Activity 5")
        self.assertEqual(latest_activities[1][1], "Test Activity 4")

    def tearDown(self):
        # Close the database connection after each test
        self.db.close()


if __name__ == '__main__':
    unittest.main()
