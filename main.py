from PIL import Image
from math import sqrt
import argparse
from tqdm import tqdm

def vector_magnitude(v: tuple):
    """
    Finds the magnitude of a given vector.
    As it turns out, the magnitude of an RGB value abstracted as vector
    works for finding a sane grayscale value.
    """

    mag = 0
    for component in v:
        mag += component ** 2
    return sqrt(mag)

def scale_vector(s, v: tuple):
    return tuple(s * x for x in v)

def dot_product(v1: tuple, v2: tuple):
    total = 0
    for i in range(len(v1)):
        total += v1[i] * v2[i]
    return total

def project_vector(b: tuple, a: tuple):
    """Project vector a onto b"""
    # Handle zero vector to avoid division by zero
    if vector_magnitude(b) == 0:
        return (0, 0, 0)
    return scale_vector(dot_product(a, b) / dot_product(b, b), b)

def integerize_vector(v: tuple):
    return tuple(int(x) for x in v)

def main():
    parser = argparse.ArgumentParser(description='Quantify image similarity using linear algebra concepts')
    parser.add_argument('image1', type=str, help='Path to the first image')
    parser.add_argument('image2', type=str, help='Path to the second image')
    args = parser.parse_args()

    img_right = Image.open(args.image1)
    print("Opened image 1")
    img_left = Image.open(args.image2)
    print("Opened image 2")

    right_rgb_list = list(img_right.getdata())
    left_rgb_list = list(img_left.getdata())
    print("Extracted RGB values")

    vector_overlay_rtl = list()
    vector_overlay_ltr = list()
    magnitude_overlay = list()
    projected_overlay = list()

    num_pixels = len(right_rgb_list)
    # Use tqdm to create a progress bar
    for i in tqdm(range(num_pixels), desc="Processing pixels"):
        px_vector_rtl = (right_rgb_list[i][0] - left_rgb_list[i][0], right_rgb_list[i][1] - left_rgb_list[i][1], right_rgb_list[i][2] - left_rgb_list[i][2])
        px_vector_ltr = scale_vector(-1, px_vector_rtl)

        projected = integerize_vector(project_vector(right_rgb_list[i], px_vector_rtl))
        projected_overlay.append(projected)

        px_vector_magnitude = vector_magnitude(px_vector_rtl)
        magnitude_overlay.append(px_vector_magnitude)

        vector_overlay_rtl.append(px_vector_rtl)
        vector_overlay_ltr.append(px_vector_ltr)

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

if __name__ == "__main__":
    main()
