import os
from PIL import Image
import sys
ext = ['jpg','jpeg','png']
files = sys.argv[1].split(',')
default_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../source/_posts/assets/')

def process_image(filename, mwidth=200, mheight=400):
    image = Image.open(default_root + filename)
    w,h = image.size
    if w<=mwidth and h<=mheight:
        print(filename,'is OK.')
        return
    # if (1.0*w/mwidth) > (1.0*h/mheight):
    #     scale = 1.0*w/mwidth
    #     new_im = image.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)
    # else:
    #     scale = 1.0*h/mheight
    #     new_im = image.resize((int(w/scale),int(h/scale)), Image.ANTIALIAS)     
    width = 666
    new_im = image.resize((width, int(width/w*h)))
    new_im.save(default_root + '/new-'+filename)
    new_im.close()

for file in files:
    if file.split('.')[-1] in ext:
        process_image(file)


