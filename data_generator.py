import os
import random

from PIL import Image, ImageFilter

from computer_text_generator import ComputerTextGenerator

def generate(index, image, text, font, out_dir, extension, width, text_color, orientation, space_width,size):

    ##########################
    # Create picture of text #
    ##########################
    image,labelLists = ComputerTextGenerator.generate(image, text, font, text_color, size, orientation, space_width)

    #####################################
    # Generate name for resulting image #
    #####################################
    
    if len(labelLists) != 0:
        image_name = '{}_{}.{}'.format(str(orientation),str(index), extension)
        # Save the image
        image.convert('RGB').save(os.path.join(out_dir, image_name))

        txt_name = '{}_{}_{}.{}'.format('gt',str(orientation),str(index),'txt')
        f = open(os.path.join(out_dir, txt_name),'w')

        for label in labelLists:
            [x0,y0,x1,y1,label] = label

            strline = str(int(x0))+','+str(int(y0))+','+str(int(x1))+','+ \
            str(int(y0))+','+str(int(x1))+','+str(int(y1))+','+str(int(x0))+ \
            ','+str(int(y1))+','+label + '\n'

            f.write(strline)

        f.close()
