from playlist import *
import math


play_list = mod_playlist(username, client_id, client_secret, redirect_uri, scope)
play_list.authorize()

def audio_data(): #returns a dictionary of audio analysis dictionaries for every track in the playlist
    data = {}
    for key in track_dict:
        id = track_dict[key]
        audio_dict = play_list.get_audio_anal(id, key)
        data[id] = audio_dict
    return data


def find_score_downwards(current_song_id, current_song_name, new_song_dict): #finds comparison scores for songs starting at the top of the playlist moving downwards
    current_dict = audio_info[current_song_id]
    data = []

    fade_out = current_dict['duration'] - current_dict['start_of_fade_out']
    fade_in = new_song_dict['end_of_fade_in']
    total_fade_time = fade_out + fade_in
    total_fade = total_fade_time

    if current_dict['tempo_confidence'] < 0.3 and new_song_dict['tempo_confidence'] < 0.3:
        if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
            total_fade /= 2
        elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.5
    elif current_dict['tempo_confidence'] < 0.3 or new_song_dict['tempo_confidence'] < 0.3:
        if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.75
        elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.25

    key = abs(current_dict['key'] - new_song_dict['key'])

    if total_fade_time <= cross_fade:
        key /= 2

    tempo = abs(current_dict['tempo'] - new_song_dict['tempo'])

    if total_fade_time <= cross_fade:
        key /= 2

    if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
        tempo /= 2
    elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
        tempo /= 1.5

    total_score = total_fade + key + tempo
    return [new_song_dict['id'], total_score, new_song_dict['Name']]

def find_score_upwards(current_song_id, current_song_name, new_song_dict): #finds comparison scores for songs starting at the bottom of the playlist moving upwards
    current_dict = audio_info[current_song_id]
    current_dict = audio_info[current_song_id]
    data = []

    fade_out = new_song_dict['duration'] - new_song_dict['start_of_fade_out']
    fade_in = current_dict['end_of_fade_in']
    total_fade_time = fade_out + fade_in
    total_fade = total_fade_time

    if current_dict['tempo_confidence'] < 0.3 and new_song_dict['tempo_confidence'] < 0.3:
        if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
            total_fade /= 2
        elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.5
    elif current_dict['tempo_confidence'] < 0.3 or new_song_dict['tempo_confidence'] < 0.3:
        if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.75
        elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
            total_fade /= 1.25

    key = abs(current_dict['key'] - new_song_dict['key'])

    if total_fade_time <= cross_fade:
        key /= 2

    tempo = abs(current_dict['tempo'] - new_song_dict['tempo'])

    if total_fade_time <= cross_fade:
        key /= 2

    if current_dict['key_confidence'] < 0.3 and new_song_dict['key_confidence'] < 0.3:
        tempo /= 2
    elif current_dict['key_confidence'] < 0.3 or new_song_dict['key_confidence'] < 0.3:
        tempo /= 1.5

    total_score = total_fade + key + tempo
    return [new_song_dict['id'], total_score, new_song_dict['Name']]





def find_best_score(direction, current_song): #looks at every score of available songs and picks the best one
    songs_left = len(track_dict) - len(used_songs)
    songs = []
    for key in audio_info:
        if key not in used_songs:
            songs += [key]

    list_of_scores = []
    if direction == 'up':
        for x in range(songs_left):
            score = find_score_upwards(current_song[1], current_song[0], audio_info[songs[x]])
            list_of_scores += [score]

    else:
        for x in range(songs_left):
            score = find_score_downwards(current_song[1], current_song[0], audio_info[songs[x]])
            list_of_scores += [score]

    min = list_of_scores[0]
    for i in list_of_scores[1:]:
        if i[1] < min[1]:
            min = i

    print(current_song[0] + "'s best match is:", min[2], 'with score', min[1])
    return min

def re_order_playlist(current_song_down, current_song_up, used_songs, audio_info): #re orders your playlist based on scoring
    songs_left = len(track_dict) - 2
    position_down = 0
    position_up = len(track_dict) - 1
    print("OK here is the current order: ")
    print()
    play_list.list_tracks(i_d)
    print()
    print("Now re-ordering your playlist...")
    iter = 1
    while len(used_songs) != len(track_dict):
        order = play_list.get_track_order(i_d)
        best1 = find_best_score('down', current_song_down)
        count1 = 0
        for x in order:
            if x == best1[0]:
                break
            else:
                count1 += 1

        play_list.re_order(i_d, count1, position_down + iter)
        used_songs += [best1[0]]
        current_song_down = [best1[2], best1[0]]

        order = play_list.get_track_order(i_d)
        best2 = find_best_score('up', current_song_up)
        count2 = 0
        for x in order:
            if x == best2[0]:
                break
            else:
                count2 += 1

        play_list.re_order(i_d, count2, position_up - iter)
        used_songs += [best2[0]]
        current_song_up = [best2[2], best2[0]]

        if iter % 10 == 0:
            play_list.authorize()

        iter += 1

    print()
    print("proccess finished here is the new order: ")
    print()
    play_list.list_tracks(i_d)



print()
print('*MAKE SURE TO TYPE EVERYTHING CORRECTLY*')
print()
playlist_to_order = input("Which playlist would you like to re-order? ")
playlists = play_list.list_playlists()
i_d = playlists[playlist_to_order]
start = input('Pick a song to start the playlist: ')
print()
end = input('Pick a song to end the playlist: ')
track_dict = play_list.get_track_ids(i_d)
order = play_list.get_track_order(i_d)

if order[0] != track_dict[start]:
    count = 0
    for x in order:
        if x == track_dict[start]:
            break
        else:
            count += 1
    play_list.re_order(i_d, count, 0)

if order[-1] != track_dict[end]:
    count = 0
    for x in order:
        if x == track_dict[end]:
            break
        else:
            count += 1
    play_list.re_order(i_d, count, len(track_dict))

current_song_down = [start, track_dict[start]]
current_song_up = [end, track_dict[end]]
used_songs = [current_song_down[1], current_song_up[1]]
cross_fade = int(input('How many seconds of crossfade do you use? '))
print()
audio_info = audio_data()
re_order_playlist(current_song_down, current_song_up, used_songs, audio_info)
