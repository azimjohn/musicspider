import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs
from pprint import pprint
import psycopg2


base_url = "https://z1.fm/"
bot_token = "your_bot_token"
telegram_url = "https://api.telegram.org/bot"+ bot_token +"/sendMessage?chat_id=@musicspider&text={}"

hostname = 'localhost'
username = 'developer'
password = 'your_db_password'
database = 'musicspider'

mydb = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

session = requests.session()
session.headers.update({'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36', 'Accept': '*/*', 'Connection': 'keep-alive', 'origin': 'https://z1.fm'})

def requests_retry_session(
    retries=5,
    backoff_factor=0.4,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_letters(base_url):

    index = requests_retry_session(session=session).get(base_url,timeout=5)

    if(index.status_code != 200):
        pass

    parsed = bs(index.text,"lxml")
    letter_urls = []
    letters = parsed.select("div.edit-letter-spacing a")

    for letter in letters:
        letter_urls.append(base_url+letter.get("href"))

    return letter_urls


def get_artists_list(letter_url):

    html = requests_retry_session(session=session).get(letter_url,timeout=5)
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

    html = requests_retry_session(session=session).get(artist_url,timeout=5)
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

    sql = "INSERT INTO z1fm (artist,song_name,image,source,base) VALUES (%s, %s, %s, %s, %s)"
    val = (artist,song_name,image,source,base)
    cursor.execute(sql,val)
    mydb.commit()
    cursor.close()
    

def crawl(base_url):

    letters = get_letters(base_url)

    for letter in letters:

        requests_retry_session(session=session).get(telegram_url.format("Started crawling letter "+letter+" 😎😎"),timeout=5)
        print("Letter url: "+letter)
        i = 1
        check = True
        letter_disabled_btn_flag = False
        while(check):
            if letter_disabled_btn_flag:
                break

            letter_url = letter + "?page=" + str(i)
            print("Letter page: "+str(i))
            letter_html = requests_retry_session(session=session).get(letter_url, timeout=5)
            i = i + 1
            
            if(letter_html.status_code != 200):
                break

            letter_parsed = bs(letter_html.text,"lxml")
            next_btn = letter_parsed.select_one("div.paging")
            if next_btn:
                if(next_btn.select_one("a.next.disabled") is not None):
                    pprint("Next btn disabled")
                    letter_disabled_btn_flag = True
            else:
                check = False

            letter_artists = get_artists_list(letter_url)
            for artist in letter_artists:
                j = 1
                checkIn = True
                disabled_btn_flag = False
                while(checkIn):
                    # Number of artist pages to crawl
                    if j > 2:
                        break

                    if disabled_btn_flag:
                        break

                    artist_url = base_url + artist["artist_url"] + "?sort=view&page=" + str(j)
                    artist_html = requests_retry_session(session=session).get(artist_url,timeout=5)
                    if(artist_html.status_code != 200):
                        break
                        
                    artist_parsed = bs(artist_html.text,"lxml")
                    next_btn = artist_parsed.select_one("div.paging")

                    if next_btn:
                        if(next_btn.select_one("a.next.disabled") is not None):
                            disabled_btn_flag = True
                    else:
                        checkIn = False

                    artist_songs = artist_parsed.select("div.songs-list-item div.song-wrap-xl div.song-xl")
                    if not artist_songs:
                        break

                    songs = get_artist_songs(artist_url)
                    for song in songs:
                        add_song(song["artist_name"],song["song_name"],artist["image"],song["song_url"],artist_url)
                    j = j + 1
                #break # 1 artist
            #break # 1 artist page
        requests_retry_session(session=session).get(telegram_url.format("Finished crawling letter "+letter+" 😎😎"),timeout=5)
        #break # 1 letter
    requests_retry_session(session=session).get(telegram_url.format("Finished successfully 🎉🥳"),timeout=5)

if __name__ == '__main__':
    crawl(base_url)

