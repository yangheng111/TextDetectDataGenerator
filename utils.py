import os
from PIL import Image

def load_dict(lang):
    """
        Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(os.path.join('dicts', lang + '.txt'), 'r', encoding="utf8", errors='ignore') as d:
        lang_dict = d.readlines()
    return lang_dict

def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """

    if lang == 'cn':
        return [os.path.join('fonts/cn', font) for font in os.listdir('fonts/cn')]
    else:
        return [os.path.join('fonts/latin', font) for font in os.listdir('fonts/latin')]

def load_img(imgdir):
    imgNames = os.listdir(imgdir)
    imgLists = []
    
    imgPaths = [os.path.join(imgdir,i) for i in imgNames]
    for imgPath in imgPaths:
        imgLists.append(imgPath)
#         im = Image.open(imgPath)
#         if im.size[0] > 0 and im.size[1] >0:
#             imgLists.append(im) 
#         else:
#             print ('Invalid image')
    return imgLists

def mat_inter(box1,box2):
    # 判断两个矩形是否相交
    # box=(xA,yA,xB,yB)
    x01, y01, x02, y02,label1 = box1
    x11, y11, x12, y12,label2 = box2
 
    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False
    
def cal_scale(img_w,img_h,txt_w,txt_h):
    scale = 1.0 #random.uniform(0.3,0.7)
    if img_w < txt_w or img_h < txt_h:
        scale = min(img_w/txt_w,img_h/txt_h)
        if scale <0.5:
            scale = random.uniform(0.2,scale-0.01)
        else:
            scale = random.uniform(0.5,scale-0.01)
    else:
        scale = min(img_w/txt_w,img_h/txt_h)
        if scale >4:
            scale = random.uniform(1.0,scale-2)
        elif scale >1:
            scale = random.uniform(1.0,scale-0.01)
        else:
            scale = random.uniform(0.3,scale-0.01)
    return scale
    