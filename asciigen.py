import numpy as np

from PIL import Image, ImageFilter

from exception import ImageTooSmall

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'._" # changed space with underscore

# 10 levels of gray
gscale2 = '@%#*+=-:._' # changed space with underscore


def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w * h))


def getMaxL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.max(im.reshape(w * h))


def covertImageToAscii(fileName, cols, scale, moreLevels, edge):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
    if edge:
        image = image.filter(ImageFilter.FIND_EDGES)
        gscale1 = gscale1[::-1] # reverse, darker background become a "lighter" char
        gscale2 = gscale2[::-1]
        #image.save("/tmp/edge.jpg")

    # store dimensions
    W, H = image.size[0], image.size[1]

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    # check if image size is too small
    if cols > W or rows > H:
        raise ImageTooSmall()

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h) if j != rows - 1 else H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w) if i != cols - 1 else W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            avg = int(getMaxL(img)) if edge else int(getAverageL(img))

            gsval = gscale1[int((avg * 69) / 255)] if moreLevels else gscale2[int((avg * 9) / 255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg


def convert_image(imgFile, cols='80', scale='0.43', moreLevels=False, edge=False):
    aimg = covertImageToAscii(imgFile, int(cols), float(scale), moreLevels, edge)
    return aimg
