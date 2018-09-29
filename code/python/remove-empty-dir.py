import os
import subprocess

videos_folder = 'D:\Video'
tv_shows_folder = 'D:\Video\TV Shows'
movies_folder = 'D:\Video\Movies'
vlc = 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'
rnm = "D:\Video\TV Shows\Rick and Morty S02E01 HDTV x264-BATV[rarbg]"

# p = subprocess.Popen([vlc,"D:\Video\TV Shows\Who Is America\S01E02.mp4"])

def delete_empty_folders(path):
    for folderName, subfolders, filenames in os.walk(path):
        for subfolder in subfolders:
            if not os.listdir(folderName + "\\" +  subfolder):
                print("Deleting: " + folderName + "\\" +  subfolder )
                os.rmdir(folderName + "\\" +  subfolder)

def delete_empty_folders2(path):
    for root, subfolders, filenames in os.walk(path):
        for subfolder in subfolders:
            file_path = os.path.join(root, subfolder)
            print("Looking at: " + file_path)
            if not os.listdir(file_path):
                print("Deleting: " + file_path)
                os.rmdir(file_path)

def delete_txt_files(path):
    for root, subfolders, filenames in os.walk(path):
        for filename in filenames:
            # print("Filename: " + filename)
            ext = filename[-4:]
            if(ext == ".txt"):
                file_path = os.path.join(root, filename)
                print("About to remove: " + file_path)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(e)

def delete_loner_thumbnails(path):
    for root, subfolders, filenames in os.walk(path):
        for filename in filenames:
            # print("Filename: " + filename)
            ext = filename[-3:]
            if(ext == ".db"):
                file_path = os.path.join(root, filename)
                parent_directory = os.path.abspath(os.path.join(file_path, os.pardir))
                contents = os.listdir(parent_directory)
                if(len(contents) == 1):
                    print("About to remove: " + file_path + "\n" + "Parent Contents: " + str(contents))
                    try:
                        os.unlink(file_path)
                    except Exception as e:
                        print(e)

class Listing:
    def __init__(self, title, file):
        self.title = title
        self.file = file

# delete_txt_files(tv_shows_folder)
# delete_empty_folders2(rnm)
# delete_loner_thumbnails(tv_shows_folder)
delete_empty_folders(tv_shows_folder)
