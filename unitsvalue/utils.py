# unitsvalue/utils.py
import requests
from bs4 import BeautifulSoup
# from unitsvalue.models import unit_value  # Adjust the import if necessary

def convert_persian_number(unit_value:str):
    """Converts a Persian/Arabic number string to a floating-point number."""
    cleaned_unit_value = unit_value.replace(',', '')
    translation_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    western_digits = cleaned_unit_value.translate(translation_table)
    return float(western_digits)

def fetch_funds_content(url):
    """Fetches the content of the funds."""
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Raises an error for bad responses
    return response

def extract_value(soup, element_id):
    """Extracts and converts a value from the specified HTML element."""
    element = soup.find(id=element_id)
    if element:
        value = element.get_text(strip=True)
        return convert_persian_number(value)  # Use the imported function
    return None

def calculate_percent(normal_value, expert_value):
    """Calculates the percentage of normal value over expert value."""
    if expert_value == 0:
        raise ValueError("Expert value cannot be zero for percentage calculation.")
    return round((normal_value / expert_value) * 100, 1)

def scrape_funds(funds):
    """Scrapes the specified funds for unit_value data."""
    try:
        response = fetch_funds_content(funds.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        normal_value = extract_value(soup, "BaseUnitsTotalNetAssetValue")
        expert_value = extract_value(soup, "SuperUnitsTotalNetAssetValue")

        if normal_value is not None and expert_value is not None:
            percent_value = calculate_percent(normal_value, expert_value)
            return percent_value  # Return the percent value for further processing
        else:
            return None  # Indicate that values could not be found
    except requests.RequestException as e:
        raise ValueError(f'Error scraping {funds.url}: {e}')

def process_funds(funds):
    """Processes the funds and returns the percent value."""
    try:
        percent_value = scrape_funds(funds)
        if percent_value is not None:
            return percent_value
        else:
            return None  # Data not found
    except ValueError as e:
        raise ValueError(f'Failed to process {funds.url}: {e}')