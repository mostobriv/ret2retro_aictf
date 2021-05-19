import random
from PIL import Image, ImageDraw
from io import BytesIO
import os

flag = None
with open('/flag.txt', 'rb') as f:
    flag = f.read().strip()

os.unlink('/flag.txt')


def chunks(it, s):
    return [it[i:i+s] for i in range(0, len(it), s)]

def encrypt(data):
    if len(data) % 5 != 0:
        data = data + b'\x00' * (5 - len(data) % 5)

    random.seed(os.urandom(16))

    result = list()
    perm1 = [1, 3, 0, 4, 2]
    key = data[:5]
    random.shuffle(key)

    for c in chunks(data, 5):
        first_step = [c[i] for i in perm1]
        second_step = [chr(key[i] ^ first_step[i]) for i in range(5)]
        result.extend(second_step)

    return ''.join(result)

def _get_norm(score):
    x_min = 0
    x_max = 0.4

    normalized = (score - 0) * (x_max - x_min) + x_min
    return round(normalized, 1)

def get_part(score):
    new_score = _get_norm(score)
    size2hide = len(flag) - int(len(flag) * new_score)
    idx = list(range(len(flag)))
    idx2hide = (random.sample(idx, size2hide))

    user_flag = list(flag)

    for i in idx2hide:
        user_flag[i] = '_'

    return f'AICTF{{%s}}' % ''.join(user_flag)

def _mix_bit_in_byte(val, shift, bit):
    val&= ~(1 << shift)

    return val | (bit << shift)

def mix_data_to_img(img_bytes, data):
    img = Image.open(BytesIO(img_bytes))
    draw = ImageDraw.Draw(img)
    w,h = img.size
    pix = img.load()

    num = int.from_bytes(data.encode(), 'big')
    cur_shift = 0
    bitsn = len(data) << 3
    end_is_reached = False

    def get_next_data_bit():
        nonlocal cur_shift, bitsn, num, end_is_reached

        if cur_shift >= bitsn:
            end_is_reached = True
            return None
        else:
            data_bit = ((1 << (bitsn - cur_shift - 1)) & num) >> (bitsn - cur_shift - 1)

        cur_shift+= 1
        return data_bit

    for y in range(h):
        for x in range(w):
            if end_is_reached:
                buffer = BytesIO()
                img.save(buffer, format='png')
                buffer.name = 'test.png'
                buffer.seek(0)
                return buffer.read()

            bit = get_next_data_bit()
            r = _mix_bit_in_byte(pix[x, y][0], 0, bit if bit is not None else (pix[x, y][0] & 1))
            bit = get_next_data_bit()
            g = _mix_bit_in_byte(pix[x, y][1], 2, bit if bit is not None else (pix[x, y][1] & (1 << 2)) >> 2)
            bit = get_next_data_bit()
            b = _mix_bit_in_byte(pix[x, y][2], 1, bit if bit is not None else (pix[x, y][2] & (1 << 1)) >> 1)


            draw.point((x,y), (r, g, b))

    buffer = BytesIO()
    img.save(buffer, format='png')
    buffer.name = 'test.png'
    buffer.seek(0)
    return buffer.read()
