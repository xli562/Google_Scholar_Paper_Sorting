from bs4 import BeautifulSoup
import pandas as pd

# Read HTML content from file with UTF-8 encoding
with open('./tbody.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all table rows
rows = soup.find_all('tr', class_='gsc_a_tr')

# Define a function to check if Constantinides is among the first three authors
def is_constantinides_among_first_three(authors_div):
    if not authors_div:
        return False
    authors_text = authors_div.text
    authors_list = authors_text.split(", ")
    # Check if 'GA Constantinides' is among the first three authors
    return any('GA Constantinides' in author for author in authors_list[:3])

# Prepare a list to hold the filtered data
filtered_data = []

for row in rows:
    # Check if the publication year is 2010 or later
    year_span = row.find('span', class_='gsc_a_h gsc_a_hc gs_ibl')
    if year_span and int(year_span.text if year_span.text != '' else 0) >= 2010:
        title_a = row.find('a', class_='gsc_a_at')
        if title_a and 'architecture' in title_a.text:
            authors_div = row.find('div', class_='gs_gray')
            if is_constantinides_among_first_three(authors_div):
                # Extract the desired information
                title = title_a.text
                authors = authors_div.text if authors_div else "No authors"
                year = year_span.text
                citations_a = row.find('a', class_='gsc_a_ac gs_ibl')
                citations = int(citations_a.text) if citations_a else 0
                # Add the extracted information to the list
                filtered_data.append([title, authors, year, citations])

# Convert the list to a DataFrame
df = pd.DataFrame(filtered_data, columns=['Title', 'Authors', 'Year', 'Citations'])

# Write the DataFrame to an Excel file
df.to_excel('filtered_articles_arch.xlsx', index=False, engine='openpyxl')
