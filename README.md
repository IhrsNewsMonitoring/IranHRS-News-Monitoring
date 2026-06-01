# IranHRS‑News‑Monitoring

This repository contains a Python‑based monitoring system designed to track human‑rights news and prison‑related events in Iran.  It offers two data‑collection modules — one for Telegram channels and another for news websites — and persists the gathered information in an SQLite database.  A lightweight web dashboard built with Streamlit displays the collected entries.

## Features

- **Telegram monitor**: Uses the Telethon library to connect to the Telegram API and iterate through messages in specified channels.  Telethon’s `iter_messages` method allows the monitor to loop over messages in a chat or channel【78046585748960†L3020-L3044】.
- **Website monitor**: Fetches pages with the requests library and extracts content with BeautifulSoup.  For example, you can use `soup.find('h1')` to extract the first heading and `soup.find_all()` or CSS selectors to pull paragraphs【224005379937597†L80-L104】.
- **SQLite storage**: Data is stored in a local SQLite database using Python’s built‑in `sqlite3` module.  Creating a connection and a table is as simple as calling `sqlite3.connect()` and `cur.execute()`【712375156206333†L132-L161】, while insert statements and commits persist new records【712375156206333†L185-L199】.
- **Web dashboard**: A Streamlit app lets you browse and filter the collected messages.  Streamlit is an open‑source framework that turns Python scripts into interactive data apps; installing it requires only a `pip install streamlit` command【202661142142377†L65-L74】 and a few lines of code.

## Project structure

```
IranHRS-News-Monitoring/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── telegram_monitor.py
│   ├── news_monitor.py
│   └── dashboard.py
├── config_example.yaml
├── requirements.txt
└── README.md
```

- **app/config.py** – Functions to load the YAML configuration.
- **app/database.py** – Creates the `messages` table and provides helper functions to insert and query records.
- **app/telegram_monitor.py** – Asynchronous monitor for Telegram channels.  It uses Telethon’s `iter_messages` to fetch messages from each channel【78046585748960†L3020-L3044】.
- **app/news_monitor.py** – Synchronous monitor for websites.  It fetches pages with requests【264029255523120†L20-L25】 and extracts titles and content with BeautifulSoup【224005379937597†L80-L104】.
- **app/dashboard.py** – Streamlit dashboard to browse stored messages.
- **config_example.yaml** – Sample configuration file showing how to define API credentials, monitored channels and websites, and database path.

## Setup

1. **Clone this repository** and navigate into it:
   ```bash
   git clone https://github.com/your‑username/IranHRS‑News‑Monitoring.git
   cd IranHRS‑News‑Monitoring
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a configuration file**:
   - Copy `config_example.yaml` to `config.yaml` and edit the values.
   - You will need a Telegram API ID, API hash and session name.  See Telethon’s documentation for how to obtain them and how to use `iter_messages` to iterate over messages【78046585748960†L3020-L3044】.
   - Define a list of Telegram channels to monitor under `telegram.channels`.
   - Define a list of websites to monitor under `news.websites`.  Each entry should specify a URL and optional CSS selectors for the title and content.

5. **Run the monitors**:
   - **Telegram**:
     ```bash
     python -m app.telegram_monitor --config config.yaml
     ```
     The first run will ask you to sign in with your Telegram phone number; Telethon will create a `.session` file for subsequent runs.
   - **Websites**:
     ```bash
     python -m app.news_monitor --config config.yaml
     ```
     Adjust the scraping logic in `app/news_monitor.py` to fit each website’s layout.

6. **Start the dashboard**:
   ```bash
   streamlit run app/dashboard.py
   ```
   The dashboard will read data from the SQLite database and display messages.  You can filter by source (telegram or website) and search within the table.

## Requirements

The main dependencies are:

- `telethon` – Telegram API client.
- `requests` – HTTP requests for websites【264029255523120†L20-L25】.
- `beautifulsoup4` – HTML parsing and extraction【224005379937597†L80-L104】.
- `streamlit` – Web dashboard framework【202661142142377†L65-L74】.
- `pandas` – Data handling for the dashboard.
- `PyYAML` – Configuration file parsing.

See `requirements.txt` for exact versions.

## Contributing

Pull requests and issues are welcome.  Please ensure any new scrapers respect the target websites’ terms of service.

## License

This project is released under the MIT License.