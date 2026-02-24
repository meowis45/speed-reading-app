import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

##split the word

def index(word):
    length = len(word)
    if length <= 1: return 0
    elif length <= 5: return 1
    elif length <= 9: return 2
    elif length <= 13: return 3
    else: return 4

def create_word_frame(word, wpm_label, width=1080, height=1920, font_size=150):
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Font path logic (standard Linux path)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    index1 = index(word)
    print(index1,word)
    part1, focus, part2 = word[:index1], word[index1], word[index1+1:]

##colour the word
    w_part1 = draw.textlength(part1, font=font)
    w_focus = draw.textlength(focus, font=font)
    start_x = (width / 2) - w_part1 - (w_focus / 2)
    start_y = (height / 2) - (font_size / 2)
    curr_x = start_x
    draw.text((curr_x, start_y), part1, font=font, fill="white")
    curr_x += w_part1
    draw.text((curr_x, start_y), focus, font=font, fill="#FF0040") # Red Focus
    curr_x += w_focus
    draw.text((curr_x, start_y), part2, font=font, fill="white")
    
##speed label
    draw.text((width/2 - 50, 200), f"{int(wpm_label)} WPM", font=small_font, fill="gray")
    return np.array(img)