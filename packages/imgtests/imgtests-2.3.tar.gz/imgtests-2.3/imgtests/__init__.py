from IPython.display import Image
d = {'условие1':display(Image('https://imgs2.imgsmail.ru/static/octavius/promo/octavius-notify-production-calendar/octavius-notify-production-calendar_light.png')), 'условие2': display(Image('https://geekpython.in/wp-content/uploads/2023/08/dynamicimg.png'))}
def find(usl):
    for key in d.keys():
        if usl in key:
            print(d[key])