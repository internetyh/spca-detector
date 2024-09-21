import requests
from bs4 import BeautifulSoup as BS

animals = ["all", "cats", "dogs", "small animals", "farm animals"]
locations = ["ashburton-centre", "auckland-centre", "hobsonville-center"]

animal = animals[1]
location = locations[1]

url = f"https://www.spca.nz/adopt?species={animal}&centres={location}&pageNum=1"

resp = requests.get(url)
soup = BS(resp.text, "html.parser")

cats = soup.find_all("li", class_="card-item card-item--adopt js-card-item--adopt grid-col m-4 xl-2b")

cat_list = list()
for cat in cats:
    name = cat.find("h3", class_="card-title").text
    breed = cat.find("h4", class_="card-subtitle card-subtitle--gender-breed").text
    age = cat.find("h4", class_="card-subtitle--age").text
    cat_list.append([name, breed, age])

with open('cats/old.txt', 'r') as f:
    old_cat_list = f.read().splitlines()

cat_string = '\n'.join([f"{cat[0]} - {cat[1]} - {cat[2]}" for cat in cat_list])
new_cat_list = cat_string.split('\n')

difference = [cat for cat in new_cat_list if cat not in old_cat_list]

with open('cats/new.txt', 'w') as f:
    f.write(cat_string)

with open('cats/old.txt', 'w') as f:
    f.write(cat_string)

with open('cats/difference.txt', 'w') as f:
    f.write('\n'.join(difference))
