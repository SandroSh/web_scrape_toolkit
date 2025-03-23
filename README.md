# Multi-Format Data Collector

A flexible Python web scraper for extracting product data from e-commerce websites. It supports data transformation into JSON and CSV formats, image downloading, pagination handling, and detailed logging.

## Features

- **Product Data Extraction**: Collects product details (name, price, image URL, rating) using customizable CSS selectors.
- **Data Transformation**: Exports data to JSON and CSV files.
- **Image Downloading**: Saves product images to a local directory.
- **Pagination**: Handles multi-page product listings automatically.
- **Logging**: Tracks progress and errors in both console and log files.

## Prerequisites

- Python 3.8+
- Required packages:
  - `requests`
  - `beautifulsoup4`
  - `lxml` (optional, for full XPath support)

## Installation

1. **Clone the Repository** 
   ```bash
   git clone https://github.com/SandroSh/web_scrape_toolkit.git
   cd web_scrape_toolkit