import webbrowser #Press F5 to run python script in Atom - Hyper can't run webbrowser
#Get the module and access things through math.what_you_want / import math
from math import pi #This imports the variable pi so you can access it directly
#Get all variables and functions directly / from math import *


# Install packages with pip `sudo pip install --upgrade youtube_dl`
# packages are installed in this location for Python2.7
# "/usr/local/lib/python2.7/dist-packages/youtube_dl/YoutubeDL.py"

class MyClass:
    def __init__(self):
        self.instanceVariable = 42

    def define_function(self):
        print("This is a function of class MyClass")
        print("This insance has a variable of " + str(self.instanceVariable))
        tuple = ('immutable', 'set', 'of', 'ordered', 'objects')
        list = ['mutable', 'set', 'of', 'ordered', 'things']
        len(list)
        map = {'name': 'Sammy', 'animal': 'shark', 'color': 'blue', 'location': 'ocean'}
        print(map['name'])
        print("Give me a slice of a tuple " + str(tuple[1:4]))
        # Getting a slice of a tuple with a stride of 2 per hop
        numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        print(numbers[1:11:2])

    def how_do_you_seperate_params(self, param1):
        print("Yes you need to put commas between parameters")


def can_a_function_have_no_params():
    print("A function can have 0 params if it is not part of a class")

def do_this_four_times():
    for i in range(4):
        print("Doing it " + str(i) + "time")

def setting_params_in_definition(passed, n="default_variable", length=" aka keyword_variable"):
    print(passed + " is a passed variable while the following may be keyword arguments :" + n + length)

def lists_are_useful():
    playlist = ['moe.', 'cheese', 'phish', 'primus', 'panic', 'keller', 'dave matthews']
    playlist.append('Umphreys Mcgee')
    popped_song = playlist.pop(0)

    # The del keyword just deletes the elements in the list. It doesn't return them like append does
    del playlist[3:]

    # Add some garbage all at once
    garbage_list = ['dave matthews'] * 10
    playlist.extend(garbage_list)

    # If you don't know the index, you can just use remove
    while('dave matthews' in playlist):
        playlist.remove('dave matthews')
    print (playlist)

    # Alpahbetize and sort lists
    playlist.sort()

    for song in playlist:
        print ("Listening to the song " + song)

    # Need indexes while traversing a list
    for i in range(len(playlist)):
        print ("Listening to song " + str(i) + " by " + playlist[i])

    delimitter = "--"
    play_join = delimitter.join(playlist)
    print (play_join)

def what_are_dictionaries_for():
    dictionary = dict()
    word_to_count_letters_of = "ajfhldflfjkashdfhaksdhfkjhsdaakjdshfkjahsdfasdfs"
    for letter in word_to_count_letters_of:
        dictionary[letter] = dictionary.get(letter, 0) + 1
    print ("Using dictionaries to count letters: ", end=" ")
    print(dictionary)

instanceOfClass = MyClass()
instanceOfClass.define_function()
# can_a_function_have_no_params()
# do_this_four_times()
# setting_params_in_definition("steve")
# setting_params_in_definition("steve", "hello", " says the new passed variable")
# lists_are_useful()
what_are_dictionaries_for()

print (webbrowser._browsers)
# webbrowser.open('http://inventwithpython.com/') # Opens a webbrowser to a page
