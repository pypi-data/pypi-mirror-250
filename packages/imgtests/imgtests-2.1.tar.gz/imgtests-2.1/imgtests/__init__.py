from IPython.display import Image
d = {'условие1':display(Image(filename='1.png')), 'условие2': display(Image(filename='2.png')), 'условие3': display(Image(filename='4.png'))}
def find(usl):
    for key in d.keys():
        if usl in key:
            print(d[key])