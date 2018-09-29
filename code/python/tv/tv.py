import os
import subprocess

videos_folder = 'D:\Video'
tv_shows_folder = 'D:\Video\TV Shows'
movies_folder = 'D:\Video\Movies'
vlc = 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'

# p = subprocess.Popen([vlc,"D:\Video\TV Shows\Who Is America\S01E02.mp4"])

for folderName, subfolders, filenames in os.walk(videos_folder):
    print('The current folder is ' + folderName)
    print('Trimmed folder is ' + folderName[9:])
    for subfolder in subfolders:
        print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
    for filename in filenames:
        print('FILE INSIDE ' + folderName + ': '+ filename)
        format = filename[-3:]
        accepted_formats = ['mp4', 'avi', 'mkv']
        if format in accepted_formats:
            fullpath = folderName + "\\" + filename
            trimmed_folder_name = folderName[9:]
            print('Trimmed folder is ' + trimmed_folder_name)
            print("Fullpath: " + fullpath)

    print('')


class Listing:
    def __init__(self, title, file):
        self.title = title
        self.file = file
