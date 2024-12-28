import os
import requests
from apiclient.discovery import build
from dotenv import load_dotenv
from urllib.parse import urlencode
import convert
import stripper


def loadENV():

    load_dotenv('.env')


def get_urls(query):
    try:
        loadENV()
        CUSTOM_SEEARCH_API_KEY = os.environ['CUSTOM_SEEARCH_API_KEY']
        resource = build('customsearch', 'v1',
                         developerKey=CUSTOM_SEEARCH_API_KEY).cse()
        result = resource.list(q=query, cx='91c9f42bb3d3d44e2').execute()
        # print(result)
        matching_urls = []
        for item in result['items']:
            matching_urls.append(item['link'])
        return matching_urls
    except:
        return ['This search query yielded No matching results']


def get_content(list_of_urls):
    loadENV()
    SCRAPER_API_KEY = os.environ['SCRAPER_API_KEY']
    linkContents = []
    # conv = converter()
    # print(list_of_urls)
    for url in list_of_urls:
        try:
            if url.endswith('.pdf'):
                # tempCorpus = stripper2.remove_tags(reqObj.text)
                file_name = "file1.pdf"
                tempCorpus = convert.download_pdf(url, file_name)
                # print(tempCorpus)
                linkContents.append(stripper.remove_tags(tempCorpus))
            else:
                params = {'api_key': SCRAPER_API_KEY, 'url': url}
                response = requests.get('http://api.scraperapi.com/',
                                        params=urlencode(params))
                # print(list_of_urls.index(url), '\n\n\n\n')
                # print(remove_tags(response.text))
                # print(remove_tags(response.text))
                linkContents.append(stripper.remove_tags(response.text))
        except:
            list_of_urls.remove(url)
            continue
    return linkContents
