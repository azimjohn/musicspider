import requests
from bs4 import BeautifulSoup as bs


session = requests.session()
session.headers.update({'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36', 'Accept': '*/*', 'Connection': 'keep-alive', 'origin': 'https://z1.fm'})

session.get("https://z1.fm")


def search(query):
    url = f"https://z1.fm/mp3/search?keywords={query}&sort=views"
    html = session.get(url)
    parsed = bs(html.text, "lxml")
    songs = []
    songs_elem = parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl")

    for song in songs_elem:
        name = song.select_one("div.song-content div.song-name a").text.strip()
        if "edit" in name.lower() or "remix" in name.lower():
            continue

        songs.append(
            {
                # "artist" : song.select_one("div.song-content div.song-artist a").text.strip(),
                "name" : name,
                "url" : "https://z1.fm/download/"+song.get("data-play")
            }
        )

    return songs
