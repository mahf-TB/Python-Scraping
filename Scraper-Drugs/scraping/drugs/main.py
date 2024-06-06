import requests
from bs4 import BeautifulSoup
from scraping.drugs.bs_drugs import Drugs

import json
import pandas as pd

def get_contentUrl(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        return BeautifulSoup(res.content , 'html.parser')
  
def get_drugsUrl(url): 
    res = requests.get(url['link'])
    res.encoding = 'utf-8'
    if res.status_code == 200:
        return BeautifulSoup(res.content , 'html.parser')
 
def get_ContentInfo(Link):
    res = requests.get(Link['link'])
    res.encoding = 'utf-8'
    if res.status_code == 200:
        return BeautifulSoup(res.content , 'html.parser')
      
####################################################
def default(args):
    url = "https://www.drugs.com/drug_information.html"
    res = requests.get(url)
    res.encoding = 'utf-8'

    if res.status_code == 200:
        soup = BeautifulSoup(res.content , 'html.parser')
        drug = Drugs()
        links_az = drug.drugs_AZ(soup)
        nameAndLinks = []
        
        
        for link in links_az[:7]:
            content = get_contentUrl(link['link'])
            drug_alpha = drug.get_Drugs(content) 
            for all in drug_alpha[:2]:
                soup1 = get_drugsUrl(all)
                namedrugs = drug.get_drug_names(soup1)
                for drug1 in namedrugs:    
                    nameAndLinks.append(drug1)
                    
                    
        data = nameAndLinks[:int(args[0])]       
        print(len(data))
        # 
        incre = 0
        allDrug = []
        
        for drugLink in data:    
            content = get_ContentInfo(drugLink)  
            infoDrug = drug.drugs_Info(content)
            incre +=1
            percent_complete = (incre) / len(data) * 100
            
            print(f"Progression de {incre}/{len(data)} : {percent_complete:.2f}%", end='\r')
            
            if infoDrug:
                drug_info =  {
                        'drug_name': drugLink['name'],
                        'reviews': infoDrug
                    } 
                allDrug.append(drug_info)
                
        print(f"Téléchargement {incre}/{len(data)} terminé: 100%") 
        
        # Préparation des données
        drug_names = [entry["drug_name"] for entry in allDrug]
        notes = [entry["reviews"]["note"] for entry in allDrug]
        comments = [entry["reviews"]["comments"] for entry in allDrug]

        # Créer un DataFrame
        df_reviews = pd.DataFrame({
            'drug_name': drug_names,
            'note': notes,
            'comments': comments
        })
        # df = pd.json_normalize(allDrug)  
        # df_reviews = df[['drug_name', 'reviews.note', 'reviews.comments']]
        # df_reviews.columns = ['drug_name', 'note', 'comments']
        print(df_reviews)
        
        return df_reviews
            
        
        


    