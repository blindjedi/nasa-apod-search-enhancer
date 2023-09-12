# Exercise with NASA and Google Search APIs

This script performs the following tasks:

1. Makes an API call to NASA's Astronomy Picture of the Day (APOD) API at `https://api.nasa.gov/planetary/apod` to retrieve the APOD image and information.

2. Uses the title from the APOD response to make an API call to Google Custom Search API, searching for related information and images at `'https://www.googleapis.com/customsearch/v1'`.

3. Combines the results from both API calls into a dictionary.

4. Prints the combined results, including the APOD information and relevant Google search results.

## Dependencies

To run this script, you need the following dependencies:

- `requests==2.31.0`
- `python-dotenv==1.0.0`
- `pytest==7.1.3`

## Setup

Before running the script, make sure to set up your environment variables by creating a `.env` file with the following variables:

- `nasa_api_key`: Your NASA API key.
- `google_api_key`: Your Google API key.
- `search_engine_id`: Your Google Custom Search Engine ID.


### Google Custom Search JSON API

https://developers.google.com/custom-search/v1/overview
1. Create API Key
2. Create Programmable Search Engine

Set what to search to Search the entire web


### Example using virtual environment

Create a Virtual Environment
```bash
python -m venv venv
```

Activate the Virtual Environment (macOS)
```bash
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

## Usage

Test
```bash
python -m pytest apod_google_dearch_combiner.py
```

Run
```bash
python apod_google_search_combiner.py
```


