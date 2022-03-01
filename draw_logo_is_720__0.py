import os
import sys
import glob

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from point_2d import Point2D as P, Rect as R

class Config:
    FONT_PATH = 'font/ubuntu/Ubuntu-C.ttf'
    FONT_SIZE = 480
    LOGO_SIZE_BIG = 720
    LOGO_SIZE = 64
    LOGO_TEXT = 'IS'
    BG_COLOR = (255, 255, 255, 128)
    FG_COLOR = (32, 32, 32, 16)
    PADDING = 80
    PADDING_X = 160
    RADIUS = 240
    LOGO_OFFSET = (60, 60)
    
    

    
# ---
def draw_logo_0(c:Config)->Image:
    img = Image.new(mode='RGBA', 
        size=(c.LOGO_SIZE_BIG, c.LOGO_SIZE_BIG),
        color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        c.FONT_PATH, c.FONT_SIZE, 
        layout_engine=ImageFont.LAYOUT_RAQM)
    text_size = draw.textsize(c.LOGO_TEXT, font=font)
    
    base_center_p = P(c.LOGO_SIZE_BIG // 2, c.LOGO_SIZE_BIG // 2)
    text_r = base_center_p.center_extend(text_size)
    outer_r = text_r.center_extend(P(c.PADDING)).center_extend(P(c.PADDING_X, 0))
    draw.rounded_rectangle(outer_r, fill=c.BG_COLOR, radius=c.RADIUS)
    draw.text(base_center_p, c.LOGO_TEXT,
        anchor='mm', font=font, fill=c.FG_COLOR)
    return img

if __name__ == '__main__':
    c = Config()
    img_logo = draw_logo_0(c)
    img_logo.save('img/logo_is_720__0.png')