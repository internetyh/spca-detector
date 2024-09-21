import requests
from bs4 import BeautifulSoup as BS

def get_animals(animal, location):
    url = f"https://www.spca.nz/adopt?species={animal}&centres={location}&pageNum=1"

    resp = requests.get(url)
    soup = BS(resp.text, "html.parser")

    animals = soup.find_all("li", class_="card-item card-item--adopt js-card-item--adopt grid-col m-4 xl-2b")

    animal_list = list()
    for aanimal in animals:
        name = aanimal.find("h3", class_="card-title").text
        breed = aanimal.find("h4", class_="card-subtitle card-subtitle--gender-breed").text
        age = aanimal.find("h4", class_="card-subtitle--age").text
        animal_list.append([name, breed, age])

    with open(f'{animal}/{location}/old.txt', 'r') as f:
        old_animal_list = f.read().splitlines()

    animal_string = '\n'.join([f"{cat[0]} - {cat[1]} - {cat[2]}" for cat in animal_list])
    new_animal_list = animal_string.split('\n')

    difference = [cat for cat in new_animal_list if cat not in old_animal_list]

    with open(f'{animal}/{location}/new.txt', 'w') as f:
        f.write(animal_string)

    with open(f'{animal}/{location}/old.txt', 'w') as f:
        f.write(animal_string)

    with open(f'{animal}/{location}/difference.txt', 'w') as f:
        f.write('\n'.join(difference))
