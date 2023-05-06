from PIL import Image, ImageChops, ImageOps, ImageMath
import numpy as np
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

def apply_filter(image):
    Img = image

    result_img = Image.new('RGB', Img.size)
    w, h = Img.size
    maska = [[0,0,0],[0,1,-1],[0,0,0]]

    for i in range(1, w-1):
        for j in range(1, h-1):
            tmp_r = 0
            tmp_b = 0
            tmp_g = 0
            for k in range(-1,2):
                for l in range(-1, 2):
                    r,g,b=Img.getpixel((i+k, j+l))
                    tmp_r+=r*maska[k+1][l+1]
                    tmp_g+=g*maska[k+1][l+1]
                    tmp_b+=b*maska[k+1][l+1]
            result_img.putpixel((i,j),(tmp_r, tmp_g, tmp_b))

    return result_img
    
    
def linear_transform(image, a, k):
    """
    Przeprowadza transformację liniową obrazu z korekcją jasności.
    
    :param image_path: ścieżka do obrazu wejściowego
    :param a: mnożnik składowych pikseli
    :param b: stała wartość dodawana do każdej składowej piksela
    :return: ztransformowany obraz jako obiekt klasy Image
    """
    # Wczytaj obraz wejściowy
    img = image

    # Utwórz pusty obraz wyjściowy
    result_img = Image.new('RGB', img.size)

    # Przetwórz każdy piksel obrazu wejściowego
    for x in range(img.width):
        for y in range(img.height):
            # Pobierz składowe piksela
            r, g, b = img.getpixel((x, y))

            # Wykonaj transformację liniową
            r = int(a * r + k)
            g = int(a * g + k)
            b = int(a * b + k)

            # Ogranicz wartości składowych do przedziału [0, 255]
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            # Ustaw składowe piksela na obrazie wyjściowym
            result_img.putpixel((x, y), (r, g, b))

    return result_img

def better_linear_transform(image, a, k):
    arr1 = np.array(image)
    result_arr =a*arr1+k
    result_arr = np.clip(result_arr, 0, 255)
    # print(np.max(result_arr, axis=0))
    merged_image = Image.fromarray(result_arr.astype('uint8'))
    #merged_image = Image.eval(merged_image, lambda x: min(x / 255, 1) * 255)
    return merged_image

def better_power_transform(image, a, k):
    arr1 = np.array(image)
    result_arr =a*(arr1**(k/100))
    result_arr = np.clip(result_arr, 0, 255)
    # print(np.max(result_arr, axis=0))
    merged_image = Image.fromarray(result_arr.astype('uint8'))
    #merged_image = Image.eval(merged_image, lambda x: min(x / 255, 1) * 255)
    return merged_image


def create_negative_image(image):
    # Utwórz nowy obraz o takim samym rozmiarze jak oryginał
    neg_image = Image.new('RGB', image.size)

    # Iteruj po pikselach i ustaw wartości RGB na odwrotność
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = image.getpixel((x, y))
            neg_r = 255 - r
            neg_g = 255 - g
            neg_b = 255 - b
            neg_image.putpixel((x, y), (neg_r, neg_g, neg_b))
            

    return neg_image

def better_negative_image(image):
    arr1 = np.array(image)
    result_arr =255-arr1
    result_arr = np.clip(result_arr, 0, 255)
    merged_image = Image.fromarray(result_arr.astype('uint8'))
    merged_image = Image.eval(merged_image, lambda x: min(x / 255, 1) * 255)
    return merged_image


def merge_images_additive(image1, image2, tryb, alpha):
    # Konwertujemy oba obrazy do trybu "RGB"
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")
    
    # Łączymy obrazy w trybie sumy
    if (tryb == 0): # 'Additive'):
        merged_image = ImageChops.add(image1, image2)
    if (tryb == 1): # 'Subtractive'):
        merged_image = ImageChops.subtract(image1, image2)
    if (tryb == 2): # 'Difference'):
        merged_image = ImageChops.difference(image1, image2)
    if (tryb == 3): # 'Multiply'):
        merged_image = ImageChops.multiply(image1, image2)
    if (tryb == 4): # 'Screen'):
        merged_image = ImageChops.screen(image1, image2)
    if (tryb == 5): # 'Negation'):
        image1 = ImageOps.invert(image1)
        image2 = ImageOps.invert(image2)
        merged_image = ImageChops.screen(image1, image2)
        merged_image = ImageOps.invert(merged_image)
    if (tryb == 6): # 'Darken'):
        merged_image = ImageChops.darker(image1, image2)         
    if (tryb == 7): # 'Lighten'):
        merged_image = ImageChops.lighter(image1, image2)
    if (tryb == 8): # 'Exclusion'):
        dst_mode, color_pair, alpha_pair = split_separate_blend(image1, image2)

        bands = []
        for a, b in color_pair:
            bands.append(ImageMath.eval("func(float(a), float(b))", func=lambda a,b: a + b - ((2.0 * a * b) / 255.0), a=a, b=b).convert("L"))

        color_mode = dst_mode if dst_mode not in ("RGBA", "LA") else dst_mode[:-1]
        merged_image = Image.merge(color_mode, bands)
    if (tryb == 9): # 'Overlay'):
        merged_image = ImageChops.overlay(image1, image2)
    if (tryb == 10): # 'Hard light'):
        merged_image = ImageChops.hard_light(image1, image2)
    if (tryb == 11): # 'Soft light'):
        merged_image = ImageChops.soft_light(image1, image2)
    if (tryb == 12): # 'Color dodge'):
        dst_mode, color_pair, alpha_pair = split_separate_blend(image1, image2)

        bands = []
        for a, b in color_pair:
            bands.append(ImageMath.eval("func(float(a), float(b))", func=lambda a,b: (a / (255 - b)) * 255.0 + (b == 255)*255, a=a, b=b).convert("L"))

        color_mode = dst_mode if dst_mode not in ("RGBA", "LA") else dst_mode[:-1]
        merged_image = Image.merge(color_mode, bands)
    if (tryb == 13): # 'Color burn'):
        dst_mode, color_pair, alpha_pair = split_separate_blend(image1, image2)

        bands = []
        for a, b in color_pair:
            bands.append(ImageMath.eval("func(float(a), float(b))", func=lambda a,b: (1.0 - ((1.0 - a / 255.0) / b / 255.0)) * 255.0 * (b != 0), a=a, b=b).convert("L"))

        color_mode = dst_mode if dst_mode not in ("RGBA", "LA") else dst_mode[:-1]
        merged_image = Image.merge(color_mode, bands)
    if (tryb == 14): # 'Reflect'):
        image2 = image2.resize(image1.size)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result_arr = (arr1**2)*(1-arr2)
        result_arr = np.clip(result_arr, 0, 255)
        merged_image = Image.fromarray(result_arr.astype('uint8'))
    if (tryb == 15): # 'Transparency'):
        image2 = image2.resize(image1.size)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result_arr = (1 - alpha) * arr2 + alpha * arr1
        merged_image = Image.fromarray(result_arr.astype('uint8'))
        


    
    # Normalizujemy wartości pikseli, aby uniknąć nasycenia
    merged_image = Image.eval(merged_image, lambda x: min(x / 255, 1) * 255)
    
    return merged_image



def split_separate_blend(cb, cs):
    """
    :type cb: Image.Image
    :type cs: Image.Image
    :rtype: str, generator[Image.Image, Image.Image], (Image.Image, Image.Image)
    """
    cbc, cba = _split_color_and_alpha(cb)
    csc, csa = _split_color_and_alpha(cs)
    alpha_pair = (cba, csa)

    if cb.mode == cs.mode:
        dst_mode = cb.mode
        color_pair = zip(cbc, csc)
    else:
        dst_mode = cb.mode if len(cbc) >= len(csc) else cs.mode
        if dst_mode in ("RGB", "L"):
            dst_mode += "A" if cba else ""
        last_band = cbc[-1] if len(cbc) < len(csc) else csc[-1]
        color_pair = zip_longest(cbc, csc, fillvalue=last_band)

    return dst_mode, color_pair, alpha_pair


def _split_color_and_alpha(img):
    """
    :type img: Image.Image
    :rtype: (tuple(Image.Image), Image.Image)
    """
    if img.mode == "RGBA":
        r, g, b, a = img.split()
        return (r, g, b), a
    elif img.mode == "LA":
        l, a = img.split()
        return (l,), a

    bands = img.split()
    return bands, None