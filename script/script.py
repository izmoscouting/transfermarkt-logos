import requests

import pandas as pd


import time

from random import uniform
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Ouverture du dataframe
df = pd.read_excel('../files/teams/FBREF_Team_raw_stats.xlsx')


for x in df.values:
    
    #Ouverture du chromium
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome(options=options)

    #Gestion des exceptions/noms pas trouvés dans la barre de recherche

    if x[114] == 'CD Toluca':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Toluca')
    elif x[115] == 'Liga MX, Clausura':
        continue
    elif x[114] == 'St.Louis City':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Louis City')
        
    elif x[114] == 'VfL Bochum 1848':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Vfl Bochum')

    elif x[114] == 'Borussia M\'gladbach':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Gladbach')
    elif x[114] == 'RC Sporting Charleroi':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Charleroi')
    elif x[114] == 'K. Beerschot V.A.':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Beerschot')
    elif x[114] == 'Sporting Braga':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Braga')
    elif x[114] == 'Instituto De Córdoba':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Instituto')
    elif x[114] == 'Club Atlético Unión de Santa Fe':
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Santa Fe')
    elif x[114].startswith('1. '):
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={x[114].replace("1. ", "")}')
    else:
        driver.get(f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={x[114]}')
    
    
    #Gestion du cookie popup
    try:
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sp_message_iframe_953358"]'))
        )
        driver.switch_to.frame(iframe)
        deny = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[3]/div[1]/div/button')))
        deny.click()
        driver.switch_to.default_content()
    except:
        driver.refresh()
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sp_message_iframe_953358"]'))
        )
        driver.switch_to.frame(iframe)
        deny = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[3]/div[1]/div/button')))
        deny.click()
        driver.switch_to.default_content()

    
    #Aller sur la page de l'équipe depuis le moteur de recherche

    try:
        box_photo = WebDriverWait(driver, uniform(3,5)).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/a')))
        box_photo.click()

    except Exception as e:
        try:
            box_photo = WebDriverWait(driver, uniform(3,5)).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yw1"]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/a')))
            driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 120);", box_photo)
            box_photo.click()
        except Exception as e:
            box_photo = WebDriverWait(driver, uniform(3,5)).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yw2"]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/a')))
            driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 120);", box_photo)
            box_photo.click()

    #Récupérer le logo de l'équipe depuis sa page transfermarkt

    try:
        photo = WebDriverWait(driver, uniform(3,5)).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="tm-main"]/header/div[4]/img'))) 
        driver.execute_script("window.stop();")
        src = photo.get_attribute('src')
        driver.quit()
    except Exception:
        photo = driver.find_element(by=By.XPATH, value='//*[@id="tm-main"]/header/div[3]/img')
        driver.execute_script("window.stop();")
        src = photo.get_attribute('src')
        driver.quit()
    
    #Récupérer la photo pour pouvoir l'enregistrer
    response = requests.get(src,stream=True)
    # Chemin complet du fichier
    file_path = f'../logos/{x[115]}/{x[114]}.png'

    # Extraire le répertoire du chemin
    directory = os.path.dirname(file_path)

    # Créer le répertoire s'il n'existe pas déjà
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        print(f'{file_path} téléchargé')
    
    time.sleep(uniform(5,8))