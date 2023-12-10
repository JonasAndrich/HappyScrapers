#bildungsurlaub-hamburg.de
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline
import time
import random

page = 0
titlelist = []
anbieterlist = []
linklist = []
resultarea = []
ortlist = []


while page != 4680:
    #url = f"https://bildungsurlaub-hamburg.de/search?q=Spanisch&offset={page}"
    url = f"https://bildungsurlaub-hamburg.de/search?qtrigger=h&offset={page}"
    print(url)
    page = page + 20
    
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")
    #print(soup)
    for td in soup.find_all('td', class_="wisy_kurstitel"):
        title = td.get_text(strip=True)
        #print(title)
        
        titlelist.append(title)
        
        subpage = td.a.get('href')
        
        
        linkurl = r"https://bildungsurlaub-hamburg.de/"+subpage
        
        #print(linkurl)

        linklist.append(linkurl)
        time.sleep(random.uniform(5, 10))
        subresponse = requests.get(linkurl)
        subhtml = subresponse.content
        subsoup = bs(subhtml, "lxml")
        #print(subsoup)
        kursinfo = subsoup.find("div", {"id": "wisy_resultcol1"})
        kursinfo =kursinfo.get_text()

        #print(kursinfo)
        resultarea.append(kursinfo)
        
        
        try:
            ort = subsoup.find(text="Ort/Bemerkungen").findNext('td').get_text()
        except:
            ort = None
        ortlist.append(ort)

    for td in soup.find_all('td', class_="wisy_anbieter"):
        anbieter = td.get_text(strip=True)
        anbieterlist.append(anbieter)  
        

        
        #print (anbieter)

        
        
d = {'Titel':titlelist, "Ort": ortlist, 'Anbieter':anbieterlist, 'Link':linklist, "Beschreibung" : resultarea, }
df = pd.DataFrame(d, columns=['Titel',"Ort", 'Anbieter','Link', "Beschreibung"])



from datetime import datetime
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d%H%M%S")

df.to_excel(date_time + "_KurseAlles.xlsx")