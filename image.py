# функция перевода картинок из одного формата в другой
from PIL import Image
def convert_img(filename, fr, to):
    inp = 'cache/images/' + filename + '.' + fr
    out = 'cache/converted/' + filename + '.' + to
    img = Image.open(inp)
    img.save(out)
    return out
