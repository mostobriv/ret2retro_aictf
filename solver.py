from PIL import Image
import sys



def chunks(it, s):
    return [it[i:i+s] for i in xrange(0, len(it), s)]

def main(argc, argv):
    if argc != 2:
        return 0

    img = Image.open(argv[1])
    w,h = img.size
    pix = img.load()
    flag = ''

    for y in range(h):
        for x in range(w):
            flag+= str(pix[x, y][0] & 1)
            flag+= str((pix[x, y][1] & (1 << 2)) >> 2)
            flag+= str((pix[x, y][2] & (1 << 1)) >> 1)


    real_flag = str()
    for c in chunks(flag, 8):
        real_flag+= chr(int('0b'+c, 2))

    print real_flag[:real_flag.index('}')+1]


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))