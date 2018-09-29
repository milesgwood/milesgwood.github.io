import os, eyed3

# You can manually check the tags from cmd
# eyeD3 "D:\Music\Tenacious D\Wonderboy ( with lyrics )\00-ACiA1TX0tvA.mp3"
# eyeD3 "C:\Users\miles\Dropbox\New Music\00-20CTa043IA.mp3"

# When I download songs from youtube they lack all the tags they should have.
# This walks through just downloaded songs and corrects the missing tags.
def walk_through_new_music():
    global mp3path
    for path, subdirs, files in os.walk(r'C:\Users\miles\Dropbox\New Music'):
       for filename in files:
         mp3path = os.path.join(path, filename)
         if mp3path[-4:] == ".mp3":
             print(filename)
             decide_where_parsed_song_data_goes(parse_song_data(filename))

# Adds the song data assuming the structure of Artist - Song
def decide_where_parsed_song_data_goes(song_data):
    # As a default, set the title
    set_title(song_data[0])
    set_artist(song_data[0])
    set_album("Youtube Downloads")
    # Check if we have more than one piece of data
    if len(song_data) > 1:
        set_artist(song_data[0])
        set_title(song_data[1])
    # We have artist and more
    if len(song_data) > 2:
        set_title((" ".join(song_data)))

# Gets the song data from the filename
def parse_song_data(filename):
    song_data = filename.split("-") #Split on the -
    song_data = [x.strip(' ') for x in song_data] #Remove the white space
    song_data = song_data[:-1] #Get rid of the youtube url at the end of the file
    print(song_data)
    return song_data

def set_title(title):
    audiofile = eyed3.load(mp3path)
    audiofile.tag.title = title
    audiofile.tag.save()

def set_album(album):
    audiofile = eyed3.load(mp3path)
    audiofile.tag.album = album
    audiofile.tag.save()

def set_artist(artist):
    audiofile = eyed3.load(mp3path)
    audiofile.tag.artist = artist
    audiofile.tag.save()


# Takes in a string filepath example "C:\Users\miles\Dropbox\New Music\00-20CTa043IA.mp3"
def fill_in_song_title(mp3path):
    print("Updating: " + mp3path)
    audiofile = eyed3.load(mp3path)
    audiofile.tag.title = audiofile.tag.album
    if audiofile.tag.album.len() < 2:
        audiofile.tag.title = audiofile.tag.artist
    audiofile.tag.album = "Youtube Downloads"
    audiofile.tag.save()

def write_full_file_paths():
    with open("new-music.txt", "w") as a:
        for path, subdirs, files in os.walk(r'C:\Users\miles\Dropbox\New Music'):
           for filename in files:
             f = os.path.join(path, filename)
             a.write(str(f)+ os.linesep)

def read_new_song_file_names():
    with open('new-music.txt') as fp:
        for line in fp:
            if len(line) != 1:
                print(line.rstrip())
                # fill_in_song_title(line.rstrip())

def strip_trailing_newlines(line):
    if line[-1] == '\n':
        return line[:-1]
    else:
        return line


# Run this to set tags based on the filename
mp3path = "default path"
walk_through_new_music()
