import random
from utils import *
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, image, text, font, text_color, font_size, orientation, space_width):
        if orientation == 0:
            return cls.__generate_horizontal_text(image,text, font, text_color, font_size, space_width)
        elif orientation == 1:
            return cls.__generate_vertical_text(image, text, font, text_color, font_size, space_width)
        else:
            raise ValueError("Unknown orientation " + str(orientation))
    
    @classmethod
    def __generate_horizontal_text(cls, image, texts, font, text_color, font_size, space_width):
        image_font = ImageFont.truetype(font=font, size=font_size)
        txt_img = Image.open(image)
        txt_draw = ImageDraw.Draw(txt_img)
        img_w,img_h = txt_img.size
        labelLists = []
        
        for text in texts:
            words = text.split(' ')
            space_width = image_font.getsize(' ')[0] * space_width

            words_width = [image_font.getsize(w)[0] for w in words]
            text_width =  sum(words_width) + int(space_width) * (len(words) - 1)
            text_height = max([image_font.getsize(w)[1] for w in words])
            
            if text_width > img_w or text_height > img_h:
                continue
            x0 = random.randint((text_width//2)+1,img_w-(text_width//2)-1)
            y0 = random.randint((text_height//2)+1,img_h-(text_height//2)-1)
            if x0+ text_width > img_w or y0+text_height >img_h:
                continue
            if len(labelLists) == 0 :
                labelLists.append([x0,y0,x0+text_width,y0+text_height,text])
                colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
                c1, c2 = colors[0], colors[-1]

                fill = (
                    random.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
                    random.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
                    random.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
                )

                for i, w in enumerate(words):
                    txt_draw.text((x0 + sum(words_width[0:i]) + i * int(space_width), y0), w, fill=fill, font=image_font)
            else:
                box1label = [x0,y0,x0+text_width,y0+text_height,text]
                interlists = []
                for box2label in labelLists:
                    if mat_inter(box1label,box2label):
                        interlists.append('True')
                        
                if 'True' not in interlists:
                    labelLists.append([x0,y0,x0+text_width,y0+text_height,text])
                    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
                    c1, c2 = colors[0], colors[-1]

                    fill = (
                        random.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
                        random.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
                        random.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
                    )

                    for i, w in enumerate(words):
                        txt_draw.text((x0 + sum(words_width[0:i]) + i * int(space_width), y0), w, fill=fill, font=image_font)

        return txt_img,labelLists

    @classmethod
    def __generate_vertical_text(cls, image, texts, font, text_color, font_size, space_width):
        image_font = ImageFont.truetype(font=font, size=font_size)
        txt_img = Image.open(image)
        txt_draw = ImageDraw.Draw(txt_img)
        img_w,img_h = txt_img.size
        labelLists = []
        
        for text in texts:
            space_height = int(image_font.getsize(' ')[1] * space_width)

            char_heights = [image_font.getsize(c)[1] if c != ' ' else space_height for c in text]
            text_width = max([image_font.getsize(c)[0] for c in text])
            text_height = sum(char_heights)
            
            if text_width > img_w or text_height > img_h:
                continue
            x0 = random.randint((text_width//2)+1,img_w-(text_width//2)-1)
            y0 = random.randint((text_height//2)+1,img_h-(text_height//2)-1)
            
            if text_width > img_w or text_height > img_h:
                continue
                
            if len(labelLists) == 0 :
                labelLists.append([x0,y0,x0+text_width,y0+text_height,text])
                colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
                c1, c2 = colors[0], colors[-1]

                fill = (
                    random.randint(c1[0], c2[0]),
                    random.randint(c1[1], c2[1]),
                    random.randint(c1[2], c2[2])
                )

                for i, c in enumerate(text):
                    txt_draw.text((x0, y0+sum(char_heights[0:i])), c, fill=fill, font=image_font)
            else:
                box1label = [x0,y0,x0+text_width,y0+text_height,text]
                interlists = []
                for box2label in labelLists:
                    if mat_inter(box1label,box2label):
                        interlists.append('True')
                        
                if 'True' not in interlists:
                    labelLists.append([x0,y0,x0+text_width,y0+text_height,text])
                    colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
                    c1, c2 = colors[0], colors[-1]

                    fill = (
                        random.randint(c1[0], c2[0]),
                        random.randint(c1[1], c2[1]),
                        random.randint(c1[2], c2[2])
                    )

                    for i, c in enumerate(text):
                        txt_draw.text((x0, y0+sum(char_heights[0:i])), c, fill=fill, font=image_font)

        return txt_img,labelLists
