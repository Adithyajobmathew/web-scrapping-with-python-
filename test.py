import requests
all_links = []
final = [['Posting_Link', 'Price', 'Year', 'Contact', 'Class', 'Category', 'Make', 'Length', 'Propulsion Type' ,'Hull Material', 'Fuel', 'Location']]
home_url = 'http://www.boattrader.com'
search_url = 'http://www.boattrader.com/search-results/NewOrUsed-any/Type-all/Category-all/Zip-33613/Radius-4000/Sort-Length:DESC'
from bs4 import BeautifulSoup, SoupStrainer
import bs4
start = 1
while start<1000:
    r_home = requests.get(search_url)
    raw_html_home = r_home.text
    soup_home = BeautifulSoup(raw_html_home, 'html.parser')
    links = [a.attrs.get('href') for a in soup_home.select('div.info a[href]')]
    all_links += links
    count = len(links)
    start += count
    print (start)
    next_button = [a.attrs.get('href') for a in soup_home.select('a.next')]
    next_url = home_url + next_button[0]
    search_url = next_url
    single_ads = 0
    while single_ads<count:
        try:
            schema = 'http://www.boattrader.com/'
            individual_url = schema + links[single_ads]
            ind_ads = requests.get(individual_url)
            raw_html_ind = ind_ads.text
            soup_ind = BeautifulSoup(raw_html_ind, 'html.parser')
            amount = soup_ind.find_all('span', {'class':'bd-price contact-toggle'})
            price = amount[0].get_text().strip()
            year = soup_ind.find_all('span',{'class':'bd-year'})
            year_text = year[0].get_text().strip()
            contact = soup_ind.find_all('div',{'class':'contact'})
            contact_text = contact[0].get_text().strip()
            table = soup_ind.find_all('div', {'class':'collapsible open'})
            table_elem = table[0].find_all('td')
            boat_class = table_elem[0]
            boat_class_text = boat_class.get_text().strip()
            boat_category = table_elem[1]
            boat_category_text = boat_category.get_text().strip()
            boat_make = table_elem[3]
            boat_make_text = boat_make.get_text().strip()
            boat_length = table_elem[4]
            boat_length_text = boat_length.get_text().strip()
            boat_propulsion_type = table_elem[5]
            boat_propulsion_type_text = boat_propulsion_type.get_text().strip()
            boat_material = table_elem[6]
            boat_material_text = boat_material.get_text().strip()
            boat_fuel = table_elem[7]
            boat_fuel_text = boat_fuel.get_text().strip()
            boat_location = table_elem[8]
            boat_location_text = boat_location.get_text().strip()
            all_data = [[individual_url, price, year_text, contact_text, boat_class_text, boat_category_text, boat_make_text, boat_length_text, boat_propulsion_type_text, boat_material_text, boat_fuel_text, boat_location_text]]
            final += all_data
            single_ads +=1
            pass
        except:
            single_ads +=1
            continue
            

import csv
with open('output_2.csv', 'w') as fp:
    b = csv.writer(fp, delimiter=',')
    b.writerows(final)