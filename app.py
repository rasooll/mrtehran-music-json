import requests
import json
import os
from bs4 import BeautifulSoup


def get_musics(pages=1, musictype="featured"):
    musics = []
    url = "https://mrtehran.com/browse/{musictype}/page-{pages}"
    for page_number in range(1, (pages+1)):

        page = requests.get(url.format(
            musictype=musictype,
            pages=page_number
        ))
        soup = BeautifulSoup(page.content, 'html.parser')

        featured = soup.find_all(
            'div', attrs={'class': 'row musicbox-related'})
        for item in featured:
            for song in item.find_all('div', attrs={'class': 'musicbox-item'}):
                musics.append({
                    'artist': song.get('mtp-data-artist'),
                    'title': song.get('mtp-data-title'),
                    'cover': song.get('mtp-data-thumb').replace('_thumb', ''),
                    'mp3': song.get('mtp-data-song')
                })

    return musics
try:
    os.mkdir("_deploy")
except FileExistsError:
    pass

for music_type in ["featured","latest","popular"]:
    with open('_deploy/{}.json'.format(music_type), 'w') as featured:
        featured.write(json.dumps(get_musics(1,music_type), indent=2))

