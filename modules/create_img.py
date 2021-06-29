import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
import random


# Function poem_visualization
# Input: poem headline, poem text, save path
# Output: None (saves image at specified location)
def poem_visualization(poem_headline, poem_text, save_path):

    # Create image in specified size
    WIDTH = 800
    HEIGHT = 600
    img = PIL.Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=(100,100,100))

    # Add elliptic noise with specified grain size
    MAX_GRAIN_SIZE = 50
    draw = ImageDraw.Draw(img)
    for i in range(500):
        randX = random.randrange(0, WIDTH)
        randY = random.randrange(0, HEIGHT)
        brightness = random.randrange(0, 255)
        draw.ellipse((randX, randY, randX+random.randrange(0, MAX_GRAIN_SIZE), randY+random.randrange(0, MAX_GRAIN_SIZE)), fill=(brightness, brightness, brightness))
    # Blur the grain
    img = img.filter(ImageFilter.GaussianBlur(radius=10))

    # Load font and initialize draw object
    TEXT_OFFSET = 3
    largeFont = ImageFont.truetype("Consolas-Regular.ttf", 50)
    normalFont = ImageFont.truetype("Consolas-Regular.ttf", 30)
    draw = ImageDraw.Draw(img)

    # Draw offset background text in random color
    randColor = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    draw.text((50+TEXT_OFFSET, 100+TEXT_OFFSET), poem_headline, font=largeFont, fill=(randColor))
    draw.text((50+TEXT_OFFSET, 200+TEXT_OFFSET), poem_text, font=normalFont, fill=(randColor))
    # Draw front text in white
    draw.text((50, 100), poem_headline, font=largeFont, fill=(255,255,255))
    draw.text((50, 200), poem_text, font=normalFont, fill=(255,255,255))

    img.show()

    input("Do you want to save your picture?")

    # Save the image at the specified filepath
    img.save(fp=save_path)



#poem_visualization("Three aid workers who\nhad been", "The man who led the countrys Mars probe\nYou may see us cry\nbut the full extent of damage after a\n20-month journey\nWhy the Pentagon said\n\ncreated 2021-06-28", "C://Users//fdiet//Desktop//newsbot-master//testimg.jpg")


# Emboss
#img = img.filter(ImageFilter.EMBOSS)



