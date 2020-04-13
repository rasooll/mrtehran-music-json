import requests
import json
from bs4 import BeautifulSoup


def get_featured(pages=1):
    musics = []
    featured_url = "https://mrtehran.com/browse/featured/page-{}"
    for page_number in range(1,(pages+1)):

        page = requests.get(featured_url.format(page_number))
        soup = BeautifulSoup(page.content, 'html.parser')

        featured = soup.find_all('div', attrs={'class': 'row musicbox-related'})
        for item in featured:
            for song in item.find_all('div', attrs={'class': 'musicbox-item'}):
                musics.append({
                    'artist': song.get('mtp-data-artist'),
                    'title': song.get('mtp-data-title'),
                    'cover': song.get('mtp-data-thumb').replace('_thumb', ''),
                    'mp3': song.get('mtp-data-song')
                })

    return musics

with open('_deploy/featured.json', 'w') as featured:
    featured.write(json.dumps(get_featured(), indent=2))
