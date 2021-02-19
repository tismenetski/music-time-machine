from bs4 import BeautifulSoup
import requests
import constants
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Connect Spotify with Spotipy
def spotify_connection():

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            username = constants.USER_ID,
            scope=constants.SCOPE,
            redirect_uri=constants.REDIRECT_URI,
            client_id=constants.SPOTIFY_CLIENT_ID,
            client_secret = constants.SPOTIFY_CLIENT_SECRET,
            show_dialog = True,
            cache_path = 'token.txt',
    )
    )
    return sp

# Create a new playlist
def create_new_playlist(sp,playlist_name):
    sp2 = sp.user_playlist_create(
        user=constants.USER_ID,
        name=playlist_name,
        public=False,
        collaborative=False,
        description="A playlist made with a python script"
    )
    return sp2['id']

# Add Songs to the playlist
def add_songs_to_playlist(sp,playlist_id,song_list,date):
    year = date.split("-")[0]
    song_uris = []
    for song in song_list:
        result = sp.search(q=f"track:{song} year:{year}", type="track")

        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    sp.playlist_add_items(playlist_id=playlist_id, items=song_uris, position=None)


# Scrape data from www.billboard.com
def scrape(date = ""):
    BILLBOARD_URL = f"{constants.BILLBOARD_URL}/{date}"
    response = requests.get(BILLBOARD_URL)
    billboard_data = response.text
    soup = BeautifulSoup(billboard_data, 'html.parser')
    list_of_song_names = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
    print(list_of_song_names)
    song_names = []
    for song in list_of_song_names:
        name = song.getText()
        song_names.append(name)

    return song_names

def main():
    try:
        sp = spotify_connection()  # Connect to spotify
    except:
        raise Exception("Error Connecting to spotify")

    print("Hello! Welcome to the time travel machine!\n------------------------------------------")
    get_user_date = input(
        "Please enter a date in the past in the form of YYYY-MM-DD\nto create a spotify playlist of the top 100 songs in the given date:\n")
    song_list = scrape(get_user_date)[::-1]
    playlist_name = f"Music Time Machine: {get_user_date}"
    playlist_id = create_new_playlist(sp, playlist_name)
    add_songs_to_playlist(sp, playlist_id, song_list, get_user_date)

if __name__ == "__main__":
    main()