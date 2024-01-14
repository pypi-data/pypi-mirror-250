import os
import re

from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class Umbrella:

    def __init__(self, url=None, font_path="/Library/Fonts/Arial Unicode.ttf", text_data="text_data",
                 pdf_data="pdf_data"):
        self.html = None
        self.data = {}
        self.pdf_data = 'pdf_data'
        self.text_data = 'text_data'
        self.font_path = '/Library/Fonts/Arial Unicode.ttf'
        if url is None:
            self.url = (
                'https://support.umbrella.com/hc/en-us/articles/4402023980692-Data-Loss-Prevention-DLP-Test-Sample'
                '-Data-for-Built-In-Data-Identifiers')
        else:
            self.url = url

    def convert_txt_to_pdf(self, input_dir, output_dir):
        """
        Convert all text files in the input directory to PDF files in the output directory.
        :param input_dir: Directory containing text files.
        :param output_dir: Directory where PDF files will be saved.
        """
        if not os.path.exists(self.pdf_data):
            os.makedirs(self.pdf_data)

        for filename in os.listdir(self.text_data):
            if filename.endswith('.txt'):
                input_file_path = os.path.join(self.text_data, filename)
                output_file_path = os.path.join(self.pdf_data, filename.replace('.txt', '.pdf'))

                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('ArialUnicode', '', self.font_path, uni=True)
                pdf.set_font('ArialUnicode', '', 12)

                with open(input_file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        cleaned_line = line.replace('\r', '').strip()  # Strips carriage return and trailing spaces
                        pdf.cell(200, 10, txt=cleaned_line, ln=True)

                pdf.output(output_file_path)

        print("Conversion completed.")

    # Function to sanitize category names into valid filenames
    def sanitize_filename(self, name):
        return re.sub(r'\W+', '_', name)

    def initialize_browser(self):
        """
        Initialize a browser session and navigate to the specified URL.
        :return: Page source.
        """
        browser = webdriver.Chrome()
        browser.get(self.url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'Test-Samples1'))
        )
        self.html = browser.page_source
        browser.quit()

    def scrape_data(self):
        """
        Scrape data from the provided HTML.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        header = soup.find('h2', id='Test-Samples1')

        if header:
            ul_tags = header.find_next_siblings('ul')
            for ul in ul_tags:
                li_tags = ul.find_all('li', attrs={'aria-level': '1'})
                for li in li_tags:
                    category_name = li.get_text(strip=True)
                    sanitized_name = self.sanitize_filename(category_name)
                    examples_list = li.find_next_sibling('ul')
                    if examples_list and hasattr(examples_list, 'find_all'):
                        examples = [example.get_text(strip=True) for example in
                                    examples_list.find_all('li', attrs={'aria-level': '2'})]
                        self.data[sanitized_name] = examples

    def save_data_to_files(self, data):
        """
        Save scraped data to text files in the specified directory.
        :param data: Scraped data.
        """
        if not os.path.exists(self.text_data):
            os.makedirs(self.text_data)
        else:
            for file in os.listdir(self.text_data):
                os.remove(os.path.join(self.text_data, file))

        for sanitized_name, examples in self.data.items():
            file_path = os.path.join(self.text_data, f'{sanitized_name}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                for example in examples:
                    file.write(f'{example}\n')
