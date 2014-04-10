from django.shortcuts import render, get_object_or_404
from urlparse import urlparse
from careerlink.system.forms import searchForm
import requests
from bs4 import BeautifulSoup
import re

def home(request):
    scrape_results = []
   
    def extract_search_links( url, json_info ):
        r = requests.get(url)
        r_json = r.json()
        for result in r_json['results']:
            page_data = {'name': '', 'link': '', 'careerlink': '', 'location': ''}
            if 'name' in result:
                page_data['name'] = result['name']
            if 'homepage_url' in result:
                if result['homepage_url'] != None:
                    page_data['link'] = result['homepage_url']
            json_info.append(page_data)
        print(page_data['location'])
        return json_info
        
    def scrape( url ):
        try:
            r = requests.get(url, timeout=2)
            soup = BeautifulSoup(r.text)
            links = soup.find_all('a', href=True)
            for a in links:
                if re.search("career|job|employ", a.text,re.I) != None:
                    return a['href']
            return
        except Exception, e:
            print(e)

    def fixUrl( domain, path ):

        #grabs the domain from the url 
        parsed_uri = urlparse( domain )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        if re.match("\Ahttp://", path) or re.match("\Ahttps://", path):
            return path
        else:
            if re.match("\A\/", path):
                #path starts with /
                return domain[0:-1] + path

            else:
                #path doesn't start with /
                return domain + path

    if request.method == 'POST': 
        json_info = []
        form = searchForm(request.POST)
        if form.is_valid():
            search_data = re.sub(r"\s+", '+', form.cleaned_data['search_data'])
            print("New search for: " + search_data)
            for i in range(1,3):
                url = "http://api.crunchbase.com/v/1/search.js?query="+ search_data +"&api_key=h4sj33a7p3gy93brusm9xa46&page=" + str(i)
                json_info = extract_search_links( url, json_info )

            for page in json_info:
                if page['link'] != None:
                    if page['link'] != '':
                        scrape_link = scrape(page['link'])
                        if scrape_link != None:
                            page['careerlink'] = fixUrl( page['link'], scrape_link )
                            scrape_results.append(page)

    scrape_len = len(scrape_results)
    
    return render(request, 'index.html',
                {'scrape_results': scrape_results,
                 'scrape_len': scrape_len})