from PIL import Image
from math import sqrt
# from time import sleep

def vector_magnitude(v:tuple):
    """
    Finds the magnitude of a given vector.
    As it turns out, the magnitude of an RGB value abstracted as vector
    works for finding a sane grayscale value.
    """
    mag = 0
    for component in v:
        mag += component ** 2
    return sqrt(mag)

def scale_vector(s, v:tuple):
    return tuple(s * x for x in v)

def dot_product(v1:tuple, v2:tuple):
    total = 0
    for i in range(len(v1)):
        total += v1[i]*v2[i]
    return total

def project_vector(b:tuple, a:tuple):
    """Project vector a onto b"""
    # Handle zero vector to avoid division by zero
    if vector_magnitude(b) == 0:
        return (0, 0, 0)
    return scale_vector(dot_product(a, b) / dot_product(b, b), b)

def integerize_vector(v:tuple):
    return tuple(int(x) for x in v)


img_right = Image.open('images/landscape_right.jpg')
img_left = Image.open('images/landscape_left.jpg')

right_rgb_list = list(img_right.getdata())
left_rgb_list = list(img_left.getdata())

vector_overlay_rtl = list()
vector_overlay_ltr = list()
magnitude_overlay = list()
projected_overlay = list()

for i in range(len(right_rgb_list)):
    px_vector_rtl = (right_rgb_list[i][0]-left_rgb_list[i][0], right_rgb_list[i][1]-left_rgb_list[i][1], right_rgb_list[i][2]-left_rgb_list[i][2])
    px_vector_ltr = scale_vector(-1, px_vector_rtl)

    projected = integerize_vector(project_vector(right_rgb_list[i], px_vector_rtl))
    projected_overlay.append(projected)

    # Magnitude is the same for both vectors above
    px_vector_magnitude = vector_magnitude(px_vector_rtl)
    magnitude_overlay.append(px_vector_magnitude)

    vector_overlay_rtl.append(px_vector_rtl)
    vector_overlay_ltr.append(px_vector_ltr)

    # print(px_vector)
    # sleep(.2)

vector_rtl_overlay_img = Image.new('RGB', img_right.size)
vector_rtl_overlay_img.putdata(vector_overlay_rtl)
vector_rtl_overlay_img.show()

vector_ltr_overlay_img = Image.new('RGB', img_left.size)
vector_ltr_overlay_img.putdata(vector_overlay_ltr)
vector_ltr_overlay_img.show()

projected_overlay_img = Image.new('RGB', img_right.size)
projected_overlay_img.putdata(projected_overlay)
projected_overlay_img.show()

magnitude_overlay_img = Image.new('L', img_right.size)
magnitude_overlay_img.putdata(magnitude_overlay)
magnitude_overlay_img.show()

