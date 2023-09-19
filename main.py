"""
This Python program utilizes the Bored API to fetch and manage random activities.
It includes a BoredAPIWrapper class for API interaction and an ActivityDatabase class for SQLite storage.
Users can filter activities via a command line interface and save matching results in the database.
"""

import requests
import argparse
import sqlite3


class BoredAPIWrapper:
    """
    Interacts with the Bored API to fetch random activities and apply optional filters.

    Attributes:
        base_url (str): The base URL of the Bored API.
    """

    def __init__(self):
        self.base_url = "https://www.boredapi.com/api/activity"

    def get_random_activity(self, activity_type=None, participants=None, price_min=None, price_max=None,
                            accessibility_min=None, accessibility_max=None):
        """
        Fetch a random activity from the Bored API with optional filtering.

        # Args:
        #     activity_type (str): The type of activity to filter (e.g., "education").
        #     participants (int): The number of participants for the activity.
        #     price_min (float): The minimum price for the activity.
        #     price_max (float): The maximum price for the activity.
        #     accessibility_min (float): The minimum accessibility for the activity.
        #     accessibility_max (float): The maximum accessibility for the activity.

        Returns:
            dict or None: A dictionary representing the fetched activity or None if unsuccessful.
        """

        # params = {}
        # if activity_type:
        #     params["type"] = activity_type
        # if participants:
        #     params["participants"] = participants
        # if price_min:
        #     params["price_min"] = price_min
        # if price_max:
        #     params["price_max"] = price_max
        # if accessibility_min:
        #     params["accessibility_min"] = accessibility_min
        # if accessibility_max:
        #     params["accessibility_max"] = accessibility_max
        #
        # response = requests.get(self.base_url, params=params)
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class ActivityDatabase:
    """
    Manage a SQLite database for storing activity data.

    Attributes:
        db_name (str): The name of the SQLite database.
        conn (sqlite3.Connection): The database connection.
        cursor (sqlite3.Cursor): The database cursor for executing queries.
    """

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create the 'activities' table if it doesn't exist.
        """

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                activity TEXT,
                type TEXT,
                participants INTEGER,
                price REAL,
                accessibility REAL
            )
        """)
        self.conn.commit()

    def save_activity(self, activity):
        """
       Save an activity to the database.

       Args:
           activity (dict): A dictionary representing the activity to be saved.
       """

        self.cursor.execute("""
            INSERT INTO activities (activity, type, participants, price, accessibility)
            VALUES (?, ?, ?, ?, ?)
        """, (
            activity['activity'], activity['type'], activity['participants'], activity['price'],
            activity['accessibility']))
        self.conn.commit()

    def get_latest_activities(self, limit=5):
        """
        Retrieve the latest activities from the database.

        Args:
         limit (int): The maximum number of activities to retrieve.

        Returns:
         list: A list of tuples representing the latest activities.
        """

        self.cursor.execute("""
            SELECT * FROM activities
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """

        self.conn.close()


def main():
    """
    Main function to run the command-line program for fetching and managing random activities.
    """

    parser = argparse.ArgumentParser(description="Random Activity Generator")
    parser.add_argument("command", choices=["new", "list"], help="Command to execute")
    parser.add_argument("--type", help="Filter by activity type")
    parser.add_argument("--participants", type=int, help="Filter by number of participants")
    parser.add_argument("--price_min", type=float, help="Minimum price")
    parser.add_argument("--price_max", type=float, help="Maximum price")
    parser.add_argument("--accessibility_min", type=float, help="Minimum accessibility")
    parser.add_argument("--accessibility_max", type=float, help="Maximum accessibility")

    args = parser.parse_args()

    if args.command == "new":
        bored_api = BoredAPIWrapper()
        activity = bored_api.get_random_activity()

        if activity:
            # Check if the activity matches the filters
            if (not args.type or args.type == activity['type']) and \
                    (args.participants is None or args.participants == activity['participants']) and \
                    (args.price_min is None or (args.price_min <= activity['price'] <= args.price_max)) and \
                    (args.accessibility_min is None or (
                            args.accessibility_min <= activity['accessibility'] <= args.accessibility_max)):

                db = ActivityDatabase("activities.db")
                db.save_activity(activity)
                db.close()
                print("Activity saved to the database.")
            else:
                print("Activity does not match the filters.")
        else:
            print("Failed to retrieve an activity.")

    elif args.command == "list":
        db = ActivityDatabase("activities.db")
        latest_activities = db.get_latest_activities()
        db.close()
        print("Latest Activities:")
        for activity in latest_activities:
            print(activity)


if __name__ == "__main__":
    main()
