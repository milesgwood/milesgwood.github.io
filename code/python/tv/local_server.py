import http.server
import socketserver
import subprocess
import os
import logging
import cgi


videos_folder = 'D:\Video'
tv_shows_folder = 'D:\Video\TV Shows'
movies_folder = 'D:\Video\Movies'
vlc = 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'
test = "D:\Video\TV Shows\Who Is America\S01E02.mp4"
test_folder= "D:\Video\TV Shows"

PORT = 8000

current_series = "default"
split_folder = []

def create_show_listing(folder_name, f, filename):
    global current_series, split_folder
    split_folder = folder_name.split("\\")
    # print('Current folder: ' + folder_name)
    # print('Split folder: ' + str(split_folder))
    # print('Filename: ' + filename)
    # If we have more than 3 sections, we have a show "D:\Video\TV Shows\Would I Lie To You"
    if(len(split_folder) > 3):
        # Check if we have seen this series before
        if(split_folder[3] != current_series):
            if(current_series != 'default'):
                f.write('</div>')
            current_series =  split_folder[3]
            type = split_folder[2]
            type = "_".join(type.split(' '))
            f.write('<div data-type="' + type  + '" data-series="'+ current_series + '" class="show child grow ' + type + '" onclick="expand(this);">')
            add_show_cover(folder_name, f)
            add_show_title(split_folder[3], f)
            add_line_item(f, filename, folder_name)
        else:
            add_line_item(f, filename, folder_name)
    # If we have exactly 3 list items, we have a movie or other file not in a folder.
    if(len(split_folder) == 3):
        # if(split_folder[3] != current_series):
            print("!!!!! - This item needs to be in a folder")
            # if(current_series != 'default'):
                # f.write('</div>')
            # current_series =  split_folder[3]
            # type = split_folder[2]
            # type = "_".join(type)
            # f.write('<div data-type="' + type  + '" data-series="'+ current_series + '" class="child grow ' + type + '" onclick="expand(this);">')

def add_show_title(title, f):
    f.write('<div class="title-bk"><h2>'+ title +'</h2></div>')

def add_show_cover(folder_name, f):
    cover_photo = folder_name + "\\" + "cover.jpg"
    if(os.path.exists(cover_photo)):
        f.write('<img src="' + cover_photo +'"/>')
    else:
        f.write('<img id="cover_photo" data-directory="'+ folder_name + '" src="default.jpg" />')

def add_line_item(f, filename, folder):
    global split_folder
    trimmed_folder_name = folder[9:]
    folder_with_underscores = "_".join(trimmed_folder_name.split(" "))
    filename_with_underscores = "_".join(filename.split(" "))
    type_with_underscores = "_".join(split_folder[3].split(" "))
    f.write('<div id="'+ folder_with_underscores + '\\' + filename_with_underscores +'" data-type="' + type_with_underscores + '" data-series="'+ current_series +'" class="playable ' + type_with_underscores + ' " onclick="play(this);">' + filename_with_underscores[:45] + '</div>')


def build_media_library():
    global current_series, split_folder
    accepted_formats = ['mp4', 'avi', 'mkv', 'mov']
    f = open("index.html", "w+")
    f.write('<!DOCTYPE HTML><html><head><title>Video</title><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no"/><link rel="stylesheet" href="tv.min.css"/><script type="text/javascript" src="scripts.js"></script></head><body><div class="container">')
    for folder_name, subfolders, filenames in os.walk(test_folder):
        for filename in filenames:
            # print('FILE INSIDE ' + folder_name + '\\'+ filename)
            format = filename[-3:]
            if format in accepted_formats:
                create_show_listing(folder_name, f, filename)
    f.write('</div></div></body></html>')
    f.close()
    return

build_media_library()

def open_video_if_exists(path):
    remove_question_mark = path.split("?")
    remove_question_mark = remove_question_mark[1:]
    if(len(remove_question_mark) > 0):
        video = " ".join(remove_question_mark[0].split("_"))
        full_video_path = videos_folder + "\\" + video
        print("Opening Video: ", full_video_path)
        process = subprocess.Popen([vlc, full_video_path])

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print ("Request Received: ", self.path)
        open_video_if_exists(self.path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
