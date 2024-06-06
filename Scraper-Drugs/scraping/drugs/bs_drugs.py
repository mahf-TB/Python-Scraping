from bs4 import BeautifulSoup
import requests
import string


class Drugs:
    def __init__(self):
        pass

#== function ==============================================================   
    def drugs_AZ(self, soup):
        browser_AZ = soup.find('nav', class_="ddc-paging")        
        links = browser_AZ.select('ul li a')
        hrefs = []
        base_url = "https://www.drugs.com"
        for link   in links:  
            browse_AZ = {
                'Alphabet': link.text,
                'link': base_url + link.get('href')
            }  
            hrefs.append(browse_AZ)
        return hrefs
 
 
 
#== function ==============================================================        
    def get_Drugs(self, soup):
        try:
            browser_AZ = soup.find('nav', class_="ddc-paging")        
            links = browser_AZ.select('ul li a')
        except:     
            links = None           
        hrefs = []
        base_url = "https://www.drugs.com"
        if links:
            for link in links:
                browse_AZ = {
                    'alpha': link.text,
                    'link': base_url + link.get('href')
                }  
                hrefs.append(browse_AZ)
        return hrefs


#== function ==============================================================     
    def get_drug_names(self, soup):
        drugs =  soup.select('div.ddc-main-content > ul li a')
        base_url = "https://www.drugs.com"
        drugsName = []
        for drug in drugs:
            browse_AZ = {
                    'name': drug.text,
                    'link': base_url + drug.get('href')
            }  
            drugsName.append(browse_AZ)

        return drugsName
    
#== function ==============================================================    
    def drug_reviewsSideBox(self, notes):
        avis = {
            'note':None,
            'comments':None,
            'href':None,
        }  
        try:
            note = float(notes.div.b.text)
            avis['note'] = note
        except:
            avis['reviews'] = None
            
            
        try:
            reviews = notes.em.a.text.split()[0]
            reviews = ''.join(reviews.split(','))
            reviews= int(reviews)
            avis['comments'] = reviews
        except:
            avis['comments'] = None
        
        try:
            review_link = notes.select_one('div.ddc-rating-summary em a')
            href = review_link['href']
            avis['href'] = href
        except:
            avis['href'] = None
            
        return avis
    
    
#== function ==============================================================    
    def drug_reviewsTable(self,soupTable):
        avis = {
            'note':None,
            'comments':None,
            'href':None,
        } 
        try:
            tableTrs = soupTable.find('table', class_='data-list ddc-table-sortable')
            # body = tableTrs.find('tbody')
            trs = tableTrs.select('table > tr')
            for tr in trs:
                note = tr.select_one('td.rating-score div.ddc-text-right').text
                reviews = tr.select_one('td.ddc-text-nowrap a')
                review = reviews.text.split()[0]
                href = reviews.get('href')
                
            avis['note'] = float(note)
            avis['comments'] = int(''.join(review.split(',')))
            avis['href'] = href
            return avis
        except:
            print('goooo')
     

    
#== function ============================================================== 
    def drugs_Info(self, content):
        try:
            avisUser = content.find('div', class_='ddc-sidebox ddc-sidebox-rating')
            notes = avisUser.find('div',class_='ddc-rating-summary')
            em = notes.em
            if em:
                avis = self.drug_reviewsSideBox(notes)  
                return avis
            else:
                avisUser =  content.find('ul', class_='more-resources-list more-resources-list-general')
                ressource = avisUser.select('li a')
                for a in ressource:
                    review = a.text.split()[0]
                    if review == 'Reviews':
                        base_url = "https://www.drugs.com"
                        link =base_url + a.get('href')
                        res = requests.get(link)
                        res.encoding = 'utf-8'
                        if res.status_code == 200:
                            soup = BeautifulSoup(res.content , 'html.parser')
                            avis = soup.find('div', class_='responsive-table-wrap')
                            table = self.drug_reviewsTable(avis)
                            return table
        except: 
        #self.drug_reviewsTable(avis).                                                                                                                                   
           return None
        

