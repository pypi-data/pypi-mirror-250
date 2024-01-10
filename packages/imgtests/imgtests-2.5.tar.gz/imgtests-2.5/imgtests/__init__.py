from IPython.display import Image
i1 = 'https://imgs2.imgsmail.ru/static/octavius/promo/octavius-notify-production-calendar/octavius-notify-production-calendar_light.png'
i2 = 'https://geekpython.in/wp-content/uploads/2023/08/dynamicimg.png'
d = {'условие1': i1, 'условие2': i2}
def find(usl):
    for key in d.keys():
        if usl in key:
            display(Image(d[key]))