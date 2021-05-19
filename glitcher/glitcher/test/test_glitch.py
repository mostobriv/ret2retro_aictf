#!/usr/bin/env python3
import os

from PIL import Image
from glitcher.main import glitch

PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    input_path = os.path.join(PATH, "pict", "a.jpg")
    output_dir = os.path.join(PATH, "pict")
    im = Image.open(input_path)
    output = glitch(im, 0.5555)
    basename = os.path.basename(input_path)
    outname = '{}_glitch.png'.format(os.path.splitext(basename)[0])
    out_path = os.path.join(output_dir, outname)
    output.save(out_path)
    im.close()

    input_path = os.path.join(PATH, "pict", "c.jpg")
    im = Image.open(input_path)
    output = glitch(im, 0.5555)
    basename = os.path.basename(input_path)
    outname = '{}_glitch.png'.format(os.path.splitext(basename)[0])
    out_path = os.path.join(output_dir, outname)
    output.save(out_path)
    im.close()

    input_path = os.path.join(PATH, "pict", "d.jpg")
    im = Image.open(input_path)
    output = glitch(im, 0.5555)
    basename = os.path.basename(input_path)
    outname = '{}_glitch.png'.format(os.path.splitext(basename)[0])
    out_path = os.path.join(output_dir, outname)
    output.save(out_path)
    im.close()

    input_path = os.path.join(PATH, "pict", "e.png")
    im = Image.open(input_path)
    output = glitch(im, 0.5555)
    basename = os.path.basename(input_path)
    outname = '{}_glitch.png'.format(os.path.splitext(basename)[0])
    out_path = os.path.join(output_dir, outname)
    output.save(out_path)
    im.close()

    input_path = os.path.join(PATH, "pict", "f.png")
    im = Image.open(input_path)
    output = glitch(im, 0.5555)
    basename = os.path.basename(input_path)
    outname = '{}_glitch.png'.format(os.path.splitext(basename)[0])
    out_path = os.path.join(output_dir, outname)
    output.save(out_path)
    im.close()