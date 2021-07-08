import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
import random

# From internet - only for reference
color_layer = Image.new('RGBA', [500, 500], (255, 0, 255, 255))
alpha_mask = Image.new('L', [500, 500], 0)
alpha_mask_draw = ImageDraw.Draw(alpha_mask)
alpha_mask_draw.ellipse([(150, 150), (200, 200)], fill=(157))
base_layer = Image.composite(color_layer, base_layer, alpha_mask)


    