import sys
import spotipy
import spotipy.util as util

scope = 'playlist-modify-public user-library-read'

username = #your spotify username
client_id = #your client_id which can be obtained by creating a spotify web api
client_secret= #your client secret
redirect_uri= #your redirect uri, reccomended http://localhost/


class mod_playlist(): #performs a number of operations on a users spotify account
    def __init__(self, username, client_id, client_secret, redirect_uri, scope):
        self.user = username
        self.id = client_id
        self.secret = client_secret
        self.uri = redirect_uri
        self.authorized = False
        self.scope = scope
        self.token = 0

    def authorize(self): #provides an authorization token
        self.token = util.prompt_for_user_token(self.user, self.scope,client_id= self.id ,client_secret= self.secret,redirect_uri= self.uri)

        if self.token:
            print("Successfully authorized")
            self.authorized = True
        else:
            print("Can't get token for", self.user)


    def list_playlists(self): #returns a dictionary of playlists with their id's
        if self.authorized != True:
            print("You must authorize first")
            return

        playlist_dict = {}
        sp = spotipy.Spotify(auth = self.token)
        results =sp.user_playlists(self.user)
        for item in results['items']:
            name = item['name']
            id = item['id']
            playlist_dict[name] = id

        return playlist_dict

    def list_tracks(self, playlist_id): #lists the tracks in a given playlist
        if self.authorized != True:
            print("You must authorize first")
            return

        count = 0
        sp = spotipy.Spotify(auth = self.token)
        result =sp.user_playlist_tracks(self.user, playlist_id)
        for thing in result['items']:
            song = thing['track']
            print(str(count) + ".", song['name'], "-", song['artists'][0]['name'])
            count += 1

    def get_track_order(self, playlist_id): #obtains the current track order of a playlist
        if self.authorized != True:
            print("You must authorize first")
            return

        order_list = []

        sp = spotipy.Spotify(auth = self.token)
        result =sp.user_playlist_tracks(self.user, playlist_id)
        for thing in result['items']:
            song = thing['track']
            order_list += [song['id']]

        return order_list


    def re_order(self, playlist_id, mover, location): #re-orders a playlist
        if self.authorized != True:
            print("You must authorize first")
            return

        sp = spotipy.Spotify(auth = self.token)
        sp.user_playlist_reorder_tracks(username, playlist_id, mover, location)

    def get_track_ids(self, playlist_id): #returns a dictionary of tracks and their id's
        if self.authorized != True:
            print("You must authorize first")
            return

        sp = spotipy.Spotify(auth = self.token)
        result =sp.user_playlist_tracks(self.user, playlist_id)
        dict = {}
        for item in result['items']:
            track_obj = item['track']
            namey = track_obj['name']
            track_id = track_obj['id']
            dict[namey] = track_id
        return dict

    def get_audio_anal(self, track_id, song_name): #returns a dictionary of audio analysis values used for computation and comparison
        if self.authorized != True:
            print("You must authorize first")
            return

        audio_dict = {'Name' : song_name, 'id' : track_id}
        sp = spotipy.Spotify(auth = self.token)
        result =sp.audio_analysis(track_id)
        data1 = result['track']

        audio_dict['duration'] = float(data1['duration'])
        audio_dict['end_of_fade_in'] = float(data1['end_of_fade_in'])
        audio_dict["start_of_fade_out"] = float(data1["start_of_fade_out"])
        audio_dict['key'] = float(data1['key'])
        audio_dict['tempo'] = float(data1['tempo'])
        audio_dict['key_confidence'] = float(data1['key_confidence'])
        audio_dict['tempo_confidence'] = float(data1['tempo_confidence'])

        """data2 = result['sections'][0]
        audio_dict['tempo'] = data2['tempo']
        audio_dict['key'] = data2['key']"""

        return audio_dict
