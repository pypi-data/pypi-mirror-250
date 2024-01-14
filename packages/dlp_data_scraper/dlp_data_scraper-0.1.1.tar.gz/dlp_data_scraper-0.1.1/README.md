Thank you for sharing the GitHub repository URL. I will include this in the README.md. Here's the updated README file with the correct GitHub URL:

---

# DLP Data Scraper

DLP Data Scraper is a Python tool designed to scrape and analyze data for data loss prevention (DLP) purposes. It fetches DLP test sample data from specified URLs, saves the data in text format, and then converts these text files into PDFs. The output is suitable for benchmarking DLP systems or Generative AI Language Learning Models (GenAI LLMs) for prompt injection testing.

## Features

- Web scraping from specified URLs.
- Data extraction and saving in text format.
- Conversion of text data to PDF format, ideal for benchmarking DLP systems or GenAI LLMs.

## Installation

To install DLP Data Scraper, clone the repository and install the required packages:

```bash
git clone https://github.com/BenderScript/DLPDataScraper.git
cd DLPDataScraper/dlp_data_scraper
pip3 install -r requirements.txt
```

## Usage

To use the DLP Data Scraper:

```python
from dlp_data_scraper import Umbrella

pdf_data = "pdf_data"
text_data = "text_data"
url = ('https://support.umbrella.com/hc/en-us/articles/4402023980692-Data-Loss-Prevention-DLP-Test-Sample-Data-for'
       '-Built-In-Data-Identifiers')

scraper = Umbrella(url=url, text_data=text_data, pdf_data=pdf_data)
html_content = scraper.initialize_browser()
scraped_data = scraper.scrape_data()
scraper.save_data_to_files()
scraper.convert_txt_to_pdf()

print("Scraping and conversion to PDF completed.")
```

This example demonstrates initializing the scraper, scraping data from the specified URL, saving the data to text files, and then converting those text files to PDFs in specified directories.

## Contributing

Contributions to DLP Data Scraper are welcome. Please feel free to submit pull requests or open issues to improve the project.

---

