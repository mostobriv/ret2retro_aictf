import os
import numpy as np

import glitcher.effects

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from glitcher.effects import TransformationList

ImageType = Image.Image


STATIC_TRANSFORM = [
    (glitcher.effects.convert, {'mode': 'RGB'}),
    (glitcher.effects.split_color_channels, {'offset': 8}),
    (glitcher.effects.sharpen, {'factor': 5.0}),
    (glitcher.effects.add_transparent_pixel, {}),
    (glitcher.effects.shift_corruption, {"offset_mag" : 8, "coverage" : 0.2, "width" : 8})
]

LIBRARY_PATH = os.path.dirname(__file__)
SAMSON_FONT_PATH = os.path.join(LIBRARY_PATH, "Samson.ttf")

def add_pictured_frame(im):
    font_size = min(im.size[0], im.size[1])//20
    text_color = (256, 256, 256)
    back_color = (256, 256, 256)
    shift = min(im.size[0], im.size[1])//13
    length = 2*shift
    width = shift//8

    text = "PLAY >"
    font = ImageFont.truetype(SAMSON_FONT_PATH, size=font_size)
    location = (1.8*shift, 1.8*shift)
    d = ImageDraw.Draw(im)
    d.rectangle((shift, shift, shift + length, shift + width), fill=back_color)
    d.rectangle((shift, shift, shift + width, shift + length), fill=back_color)
    d.text(location, text, font=font, fill=text_color)

    text = "03:13:37"
    font = ImageFont.truetype(SAMSON_FONT_PATH, size=font_size)
    text_size = font.getsize(text)
    location = (im.size[0] - 1.8*shift-text_size[0], 1.8*shift)
    d = ImageDraw.Draw(im)
    d.rectangle((im.size[0] - shift - length, shift, im.size[0] - shift, shift + width), fill=back_color)
    d.rectangle((im.size[0] - shift - width, shift, im.size[0] - shift, shift + length), fill=back_color)
    d.text(location, text, font=font, fill=text_color)

    up = 1.5
    text1 = "#AICTF"
    text2 = "#ret2retro"
    font = ImageFont.truetype(SAMSON_FONT_PATH, size=font_size)
    text_size2 = font.getsize(text2)
    text_size1 = font.getsize(text1)
    location1 = (im.size[0] - 1.8*shift-text_size1[0], im.size[1] - (up+0.8)*shift - 2*text_size1[1])
    location2 = (im.size[0] - 1.8*shift - text_size2[0], im.size[1] - (up+0.8)*shift - text_size2[1])
    d = ImageDraw.Draw(im)
    d.rectangle((im.size[0] - shift - length, im.size[1] - up*shift - width, im.size[0] - shift, im.size[1] - up*shift), fill=back_color)
    d.rectangle((im.size[0] - shift - width, im.size[1] - up*shift - length, im.size[0] - shift, im.size[1] - up*shift), fill=back_color)
    d.text(location2, text2, font=font, fill=text_color)
    d.text(location1, text1, font=font, fill=text_color)

    text1 = "MOSCOW"
    text2 = "MAY. 20-22 2021"
    font = ImageFont.truetype(SAMSON_FONT_PATH, size=font_size)
    text_size = font.getsize(text)
    location2 = (1.8*shift, im.size[1] - (up+0.8)*shift-text_size[1])
    location1 = (1.8*shift, im.size[1] - (up+0.8)*shift-2*text_size[1])
    d = ImageDraw.Draw(im)
    d.rectangle((shift, im.size[1] - up*shift - width, shift + length, im.size[1] - up*shift), fill=back_color)
    d.rectangle((shift, im.size[1] - up*shift - length, shift + width, im.size[1] - up*shift), fill=back_color)
    d.text(location2, text2, font=font, fill=text_color)
    d.text(location1, text1, font=font, fill=text_color)
    return im

def add_text(im, num):
    font_size = min(im.size[0], im.size[1]) // 10
    text_color = (0, 0, 0)
    back_color = (256, 256, 256)
    text = f"HACKERNESS: {num:.3f}"
    font = ImageFont.truetype(SAMSON_FONT_PATH, size=font_size)
    text_size = font.getsize(text)

    loc_x = (im.size[0]-text_size[0])//2
    loc_y = im.size[1]-font_size*1.1

    location = (loc_x, loc_y)
    d = ImageDraw.Draw(im)
    d.rectangle((loc_x - text_size[0]*0.02, loc_y + text_size[1]*0.2, loc_x + text_size[0]*1.01, loc_y + text_size[1]*1.15), fill=back_color)
    d.text(location, text, font=font, fill=text_color)
    return im


def apply_transformations(im: ImageType, funcs: TransformationList) -> ImageType:
    transformed = im
    for func, args in funcs:
        transformed = func(transformed, **args)
    return transformed


def add_vio_filter(im):
    size = im.size
    vio = Image.new('RGBA', size, color=(100,50,220))
    im = im.convert("RGBA")

    back = np.array(im)  # Inputs to blend_modes need to be numpy arrays.
    back_float = back.astype(float)  # Inputs to blend_modes need to be floats.

    fore = np.array(vio)  # Inputs to blend_modes need to be numpy arrays.
    fore_float = fore.astype(float)  # Inputs to blend_modes need to be floats.

    # Blend images
    opacity = 0.6  # The opacity of the foreground that is blended onto the background is 70 %.
    blended_img_float = soft_light(back_float, fore_float, opacity)

    # Convert blended image back into PIL image
    blended_img = np.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    result = Image.fromarray(blended_img)
    return result


def soft_light(img_in, img_layer, opacity):
    img_in /= 255.0
    img_layer /= 255.0

    ratio = _compose_alpha(img_in, img_layer, opacity)
    comp = (1.0 - img_in[:, :, :3]) * img_in[:, :, :3] * img_layer[:, :, :3] \
           + img_in[:, :, :3] * (1.0 - (1.0 - img_in[:, :, :3]) * (1.0 - img_layer[:, :, :3]))

    ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in[:, :, :3] * (1.0 - ratio_rs)
    img_out = np.nan_to_num(np.dstack((img_out, img_in[:, :, 3])))  # add alpha channel and replace nans
    return img_out * 255.0


def _compose_alpha(img_in, img_layer, opacity):
    comp_alpha = np.minimum(img_in[:, :, 3], img_layer[:, :, 3]) * opacity
    new_alpha = img_in[:, :, 3] + (1.0 - img_in[:, :, 3]) * comp_alpha
    np.seterr(divide='ignore', invalid='ignore')
    ratio = comp_alpha / new_alpha
    ratio[ratio == np.NAN] = 0.0
    return ratio

def glitch(im, score):
    im = add_vio_filter(im)
    im = apply_transformations(im, STATIC_TRANSFORM)
    im = add_pictured_frame(im)
    im = add_text(im, score)
    return im


def glitch_bytes_io(img_bytes, score):
    im = Image.open(img_bytes)
    result = glitch(im, score)
    buffer = BytesIO()
    result.save(buffer, format='png')
    buffer.name = 'test.png'
    buffer.seek(0)
    return buffer.read()
