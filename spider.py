import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import sqlite3


base_url = "https://z1.fm/"
bot_token = "681391981:AAE2g1tFWtg712l_qKSVRO3Z-IALpLIaE-M"
telegram_url = "https://api.telegram.org/bot"+ bot_token +"/sendMessage?chat_id=@musicspider&text={}"
mydb = sqlite3.connect("data/z1.db")

############################
cursor = mydb.cursor()

sql = """
    CREATE TABLE IF NOT EXISTS "z1fm" (
        "id"    INTEGER,
        "artist"	TEXT,
        "song_name"	TEXT,
        "image"	TEXT,
        "source"	TEXT,
        "base"	TEXT,
        PRIMARY KEY("id")
    )
"""
cursor.execute(sql)
mydb.commit()
cursor.close()
###############################

session = requests.session()
session.headers.update({'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36', 'Accept': '*/*', 'Connection': 'keep-alive', 'origin': 'https://z1.fm'})

def get_letters(base_url):

    index = session.get(base_url)

    if(index.status_code != 200):
        pass

    parsed = bs(index.text,"lxml")
    letter_urls = []
    letters = parsed.select("div.edit-letter-spacing a")

    for letter in letters:
        letter_urls.append(base_url+letter.get("href"))

    return letter_urls


def get_artists_list(letter_url):

    html = session.get(letter_url)
    parsed = bs(html.text,"lxml")
    artists_list = []
    artists = parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl a.song-play")

    for artist in artists:
        image = artist.select_one("div.song-img img.lazy")
        artists_list.append({
            "image" : image.get("data-original"),
            "artist_url" : artist.get("href")
        })

    return artists_list


def get_artist_songs(artist_url):

    html = session.get(artist_url)
    parsed = bs(html.text,"lxml")
    artist_songs = []
    songs = parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl")

    for song in songs:
        artist_songs.append(
            {
                "artist_name" : song.select_one("div.song-content div.song-artist a").text.strip(),
                "song_name" : song.select_one("div.song-content div.song-name a").text.strip(),
                "song_url" : "/download/"+song.get("data-play")
            }
        )

    return artist_songs


def add_song(artist,song_name,image,source,base):
    cursor = mydb.cursor()

    sql = "INSERT INTO z1fm (artist,song_name,image,source,base) VALUES (?,?,?,?,?)"
    val = (artist,song_name,image,source,base)
    cursor.execute(sql,val)
    mydb.commit()
    cursor.close()


def crawl(base_url):

    letters = get_letters(base_url)
    for letter in letters:
        print("Letter url: "+letter)
        i = 1
        check = True
        while(check):
            letter_url = letter + "?page=" + str(i)
            print("Letter page: "+str(i))
            if(requests.get(letter_url).status_code != 200):
                break
            letter_artists = get_artists_list(letter_url)
            for artist in letter_artists:
                j = 1
                checkIn = True
                while(checkIn):
                    artist_url = base_url + artist["artist_url"] + "?sort=view&page=" + str(j)
                    artist_html = session.get(artist_url)
                    if(artist_html.status_code != 200):
                        break
                    artist_parsed = bs(artist_html.text,"lxml")
                    is_disabled = artist_parsed.select_one("div.paging")
                    artist_songs = artist_parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl")
                    if not artist_songs:
                        break
                    songs = get_artist_songs(artist_url)
                    for song in songs:
                        add_song(song["artist_name"],song["song_name"],artist["image"],song["song_url"],artist_url)
                    if(is_disabled is None):
                        break
                    if(is_disabled.select_one("a.next.disabled") is not None):
                            break
                    j = j + 1
                # break # 1 artist
            i = i + 1
            # break # 1 artist page
        session.get(telegram_url.format("Finished crawling letter "+letter+" 😎😎"))
        # break # 1 letter
    session.get(telegram_url.format("Finished successfully 🎉🥳"))


if __name__=='__main__':
    crawl(base_url)
