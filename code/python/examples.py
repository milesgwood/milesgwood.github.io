import webbrowser #Press F5 to run python script in Atom - Hyper can't run webbrowser

# Install packages with pip `sudo pip install --upgrade youtube_dl`
# packages are installed in this location for Python2.7
# "/usr/local/lib/python2.7/dist-packages/youtube_dl/YoutubeDL.py"

class MyClass:
    def __init__(self):
        self.instanceVariable = 42

    def defineFunction(self):
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


def canAFunctionHaveNoParams():
    print("A function can have 0 params if it is not part of a class")

instanceOfClass = MyClass()
instanceOfClass.defineFunction()
canAFunctionHaveNoParams()

print (webbrowser._browsers)
webbrowser.open('http://inventwithpython.com/')
