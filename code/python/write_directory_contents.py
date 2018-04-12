import os

with open("full-path.txt", "w") as a:
    for path, subdirs, files in os.walk(r'/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/sites/sorensen/files/va_politics_page'):
       for filename in files:
         f = os.path.join(path, filename)
         a.write(str(f) + os.linesep)

class MyTools:
    def write_file_path_from_docroot(self, relative_path):
        with open("relative-path.txt", "w") as a:
            for path, subdirs, files in os.walk(r'/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/sites/sorensen/files/va_politics_page'):
               for filename in files:
                 f = os.path.join(relative_path, filename)
                 a.write(str(f) + os.linesep)

    def write_img_path_from_docroot(self, relative_path):
        with open("relative-path-img.txt", "w") as a:
            for path, subdirs, files in os.walk(r'/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/sites/sorensen/files/va_politics_page'):
               for filename in files:
                 f = os.path.join(relative_path, filename)
                 a.write("<img src='" + str(f) + "'/>" + os.linesep)
    def write_img_link_path_from_docroot(self, relative_path):
        with open("relative-link-img.txt", "w") as a:
            for path, subdirs, files in os.walk(r'/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/sites/sorensen/files/va_politics_page'):
               for filename in files:
                 f = os.path.join(relative_path, filename)
                 a.write("<a class='politics-link' href='/' ><img class='grow' src='" + str(f) + "'/></a>" + os.linesep)


site = "sorensen"
relative_path = "sites/" + site + "/files/va_politics_page"
r = MyTools()
# r.write_file_path_from_docroot(relative_path)
r.write_img_link_path_from_docroot(relative_path)
