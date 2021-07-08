import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
import random


# Function make_image
# Creates rasterized visualization of poem text
# Input: Poem headline, poem text, save path
# Output: None (saves image at specified location)
def make_image(poem_headline, poem_text):

    # Create image in specified size
    WIDTH = 800
    HEIGHT = 600
    img = PIL.Image.new(mode='RGB', size=(WIDTH, HEIGHT), color=(100,100,100))

    # Add elliptic noise with specified grain size
    MAX_GRAIN_SIZE = 50
    draw = ImageDraw.Draw(img, 'RGB')
    for i in range(500):
        randX = random.randrange(0, WIDTH)
        randY = random.randrange(0, HEIGHT)
        brightness = random.randrange(0, 255)
        draw.ellipse((randX, randY, randX+random.randrange(0, MAX_GRAIN_SIZE), randY+random.randrange(0, MAX_GRAIN_SIZE)), fill=(brightness, brightness, brightness))
    
    # Create random color for background text
    randColor = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))

    # Add several ellipses in contrasting color with transparency effect
    contrastColor = get_contrast(randColor[0], randColor[1], randColor[2])
    temp_img = img.copy()
    temp_img_draw = ImageDraw.Draw(temp_img)
    for i in range(30):
        randX = random.randrange(0, WIDTH)
        randY = random.randrange(0, HEIGHT)
        temp_img_draw.ellipse((randX, randY, randX+random.randrange(0, MAX_GRAIN_SIZE * 4), randY+random.randrange(0, MAX_GRAIN_SIZE * 4)), fill=contrastColor)
    img = Image.blend(temp_img, img, 0.8)

    # Blur the background
    img = img.filter(ImageFilter.GaussianBlur(radius=10))

    # Load font and initialize draw object
    TEXT_OFFSET = 3
    largeFont = ImageFont.truetype("Consolas-Regular.ttf", 50)
    normalFont = ImageFont.truetype("Consolas-Regular.ttf", 30)
    draw = ImageDraw.Draw(img)

    # Draw offset background text
    draw.text((50+TEXT_OFFSET, 100+TEXT_OFFSET), poem_headline, font=largeFont, fill=(randColor))
    draw.text((50+TEXT_OFFSET, 200+TEXT_OFFSET), poem_text, font=normalFont, fill=(randColor))

    # Draw front text in white
    draw.text((50, 100), poem_headline, font=largeFont, fill=(255,255,255))
    draw.text((50, 200), poem_text, font=normalFont, fill=(255,255,255))

    return img


# Function save_image
# Saves an image object at specified location
# Input: Image object, savepath
# Output: None
def save_image(img, save_path):
    # Save the image at the specified filepath
    img.save(fp=save_path)


# Function show_image
# Shows an image object to the user
# Input: Image object
# Output: None
def show_image(img):
    img.show()


# Function get_contrast
# Computes the maximum contrast of a given RGB color
# Credit: User 'PM 2Ring' on Stackoverflow
# Input: r,g,b values
# Output: contrasting r,g,b values
def get_contrast(r,g,b):
    def hilo(a, b, c):
        if c < b: b, c = c, b
        if b < a: a, b = b, a
        if c < b: b, c = c, b
        return a + c
    def complement(r, g, b):
        k = hilo(r, g, b)
        return tuple(k - u for u in (r, g, b))
    return complement(r,g,b)

