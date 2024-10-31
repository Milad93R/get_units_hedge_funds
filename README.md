```markdown
# Unit Hedge Funds Scraper

A sample project to scrape data from hedge funds and display it in a Django application.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Project](#running-the-project)
- [Setting Up Real-Time Data](#setting-up-real-time-data)
- [Contributing](#contributing)
- [License](#license)

## Features

- Compare unit percentages of various hedge funds.
- Convert Excel data of each hedge fund into a DataFrame.

## Technologies Used

- **Django**: Version 3.2 (or your specific version)
- **Python**: Version 3.9 (or your specific version)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Additional Libraries**: `requests`, `beautifulsoup4`, `pandas`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Milad93R/get_units_hedge_funds.git
   cd get_units_hedge_funds
   ```

2. Install Pipenv if you haven't already:

   ```bash
   pip install pipenv
   ```

3. Install project dependencies:

   ```bash
   pipenv install
   ```

4. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):

   ```bash
   python manage.py createsuperuser
   ```

## Usage

After running the project, you can access the Django admin panel at `http://127.0.0.1:8000/admin` to manage your data.

- Visit `http://127.0.0.1:8000/history_values` to view the history of scraped data and compare the unit percentages of each hedge fund.
- Visit `http://127.0.0.1:8000/live_values` to view the scraped data and compare the unit percentages of each hedge fund in real-time.

To convert Excel data of each hedge fund into a DataFrame, use the following command:

```bash
pipenv run python manage.py convert_xlsx_to_df
```

## Running the Project

To run the development server, use:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your web browser to view the application.

## Setting Up Real-Time Data

To fetch real-time data, you should set up a cron job to run the following command every 2 minutes:

1. Open your crontab for editing:

   ```bash
   crontab -e
   ```

2. Add the following line to schedule the task:

   ```bash
   */2 * * * * cd /path/to/your/project && pipenv run python manage.py update_units
   ```

   Make sure to replace `/path/to/your/project` with the actual path to your Django project.

To fetch daily data, set up another cron job:

1. Open your crontab for editing:

   ```bash
   crontab -e
   ```

2. Add the following line to schedule the daily task:

   ```bash
   0 0 * * * cd /path/to/your/project && pipenv run python manage.py save_percent_unit
   ```

   This will run the command at midnight every day.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for discussion.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Key Updates
- **Excel Data Conversion**: Added a section for converting Excel data into a DataFrame, including the appropriate command.

Feel free to modify any additional details based on your project's requirements!