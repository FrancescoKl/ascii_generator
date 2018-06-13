"""
Transform an image in ascii art
"""
import numpy as np

from PIL import Image, ImageFilter

from exception import ImageTooSmall


def get_average_l(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    image_np = np.array(image)

    # get shape
    width, height = image_np.shape

    # get average
    return np.average(image_np.reshape(width * height))


def get_max_l(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    image_np = np.array(image)

    # get shape
    width, height = image_np.shape

    # get average
    return np.max(image_np.reshape(width * height))


def covert_image_to_ascii(filename, cols, scale, morelevels, edge):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """

    # 70 levels of gray
    GSCALE1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'._"  # changed space with underscore

    # 10 levels of gray
    GSCALE2 = '@%#*+=-:._'  # changed space with underscore

    # open image and convert to grayscale
    image = Image.open(filename).convert('L')
    if edge:
        image = image.filter(ImageFilter.FIND_EDGES)
        # reverse, darker background become a "lighter" char
        GSCALE1 = GSCALE1[::-1]
        GSCALE2 = GSCALE2[::-1]
        # image.save("/tmp/edge.jpg")

    # store dimensions
    width, height = image.size[0], image.size[1]

    # compute width of tile
    width_tile = width / cols

    # compute tile height based on aspect ratio and scale
    height_tile = width_tile / scale

    # compute number of rows
    rows = int(height / height_tile)

    # check if image size is too small
    if cols > width or rows > height:
        raise ImageTooSmall()

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * height_tile)
        y2 = int((j + 1) * height_tile) if j != rows - 1 else height

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * width_tile)
            x2 = int((i + 1) * width_tile) if i != cols - 1 else width

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            avg = int(get_max_l(img)) if edge else int(get_average_l(img))

            gsval = GSCALE1[int((avg * 69) / 255)] if morelevels else GSCALE2[int((avg * 9) / 255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg


def convert_image(imagefile, cols='80', scale='0.43', morelevels=False, edge=False):
    """
    Convert an image in ascii art
    :param imagefile: path of file
    :param cols: number of cols of ascii matrix. Default to 80
    :param scale: ratio. Default to 0.43
    :param morelevels: use more simbol in ascii matrix. Default to False
    :param edge: edge detection. Default to False
    :return: ascii matrix
    """
    return covert_image_to_ascii(imagefile, int(cols), float(scale), morelevels, edge)
