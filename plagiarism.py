from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import re
from Levenshtein import distance


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)



term = input("Search Term: ")
term = term.replace(" ", "+")

text = input("Text: ")

intensity = int(input("Intensity (1-): "))

intensity = intensity*5+5

url = 'https://www.google.dz/search?q={}'.format(term)
driver.get(url)


links = driver.find_elements(By.CSS_SELECTOR, 'a')

sums = []

for link in links:
    alink = link.get_attribute('href')
    try:
        if alink.startswith("https"):
            sums.append(alink)
    except Exception as e:
        print()

driver.quit()

count = 0

for i in sums:

    if count == intensity:
        break

    response = requests.get(i)

    soup = BeautifulSoup(response.content, 'html.parser')

    web_text = soup.text
    
    min_distance = len(text)
    for j in range(len(web_text) - len(text) + 1):
        distance_i = distance(text, web_text[j:j+len(text)])
        if distance_i < min_distance:
            min_distance = distance_i
    mind = round(0.2*len(text))
    if min_distance <= mind:
        print("Most likely plagiarized!\nMake sure to check the link and see for yourself.\n")
        print(i)
        break
    else:
        print()


    count += 1