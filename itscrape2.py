from bs4 import BeautifulSoup
import requests
import csvg
it_jobs_url = 'https://www.empleosit.com.ar/browse-by-category/Desarrollador/?searchId=1621007632.0938&action=search&page=1&listings_per_page=100&view=list'

source = requests.get(it_jobs_url).text

soup = BeautifulSoup(source, 'lxml')



# Getting all the titles and URLS

urls=[]
titleList=[]
def get_each_job_url():
    for job_offer in soup.find_all('div', class_='listing-title'):
        a_all = job_offer.find_all('a')
        urls.append(a_all[1].get('href'))
        titleList.append(a_all[1].text) 

cityList=[]
descriptions = []

# Getting each job description and saving it on a csv file.

def get_each_job_description():
    
    csv_file = open('it_jobs2.csv', 'w',encoding='utf-8')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'City','descriptions'])

    index=0
    for urlJob in urls:
        print(f'Obteniendo oferta número {index} ')
        source = requests.get(urlJob).text
        soup = BeautifulSoup(source, 'lxml')
        listing = soup.find('div', class_='listingInfo')
        display_listing = listing.find_all('div', class_='displayField')
        display_listing_lenght = len(display_listing)
        city =display_listing[1].text.strip()
        cityList.append(city)
        descr = display_listing[display_listing_lenght-1].text.strip()
        descr = descr.replace('\n',"").replace('\r',"").replace("\t","")
        descriptions.append(descr)

        csv_writer.writerow([titleList[index], city,descr])
        index+=1
    csv_file.close()


get_each_job_url()

get_each_job_description()

