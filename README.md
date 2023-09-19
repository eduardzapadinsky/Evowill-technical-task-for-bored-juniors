# Random Activity Generator

This Python program utilizes the Bored API to fetch and manage random activities. Users can filter activities based on type, participants, price, and accessibility, and save matching results in a SQLite database.

## Features

- Fetch random activities with optional filters.
- Save filtered activities to a local SQLite database.
- Retrieve and display the latest saved activities.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/eduardzapadinsky/Evowill-technical-task-for-bored-juniors
   ```

2. Navigate to the project directory:

   ```shell
   cd random-activity-generator
   ```

3. Create and activate a virtual environment (optional but recommended):

   ```shell
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

### Generate and Save Random Activity

To generate and save a random activity to the database with optional filters, run the following command:

```shell
python main.py new --type education --participants 1 --price_min 0.1 --price_max 30 --accessibility_min 0.1 --accessibility_max 0.5
```

Replace the filter values as needed.

### List Latest Activities

To list the latest saved activities from the database, run the following command:

```shell
python main.py list
```
