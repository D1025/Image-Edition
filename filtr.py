import numpy as np
from PIL import Image
import math
    
def filtrRPSnp(image, tryb):
    # Konwertuj obrazek na tablicę NumPy
    img_array = np.array(image)

    # Tworzenie maski operatora Robertsa w postaci tablicy NumPy
    if tryb==0:
        maska = np.array([[0, 0, 0], [0, 1, -1], [0, 0, 0]])
    elif tryb==3:
        maska = np.array([[0, 0, 0], [0, 1, 0], [0, -1, 0]])

    # Tworzenie tablicy wynikowej o takim samym rozmiarze jak obrazek wejściowy
    result_array = np.zeros_like(img_array)

    # Przetwarzanie obrazka piksel po pikselu
    for i in range(1, img_array.shape[0] - 1):
        for j in range(1, img_array.shape[1] - 1):
            # Wyodrębnienie sąsiednich pikseli
            neighbors = img_array[i - 1:i + 2, j - 1:j + 2, :]

            # Obliczanie wartości piksela wynikowego dla każdej składowej koloru
            result_array[i, j, 0] = np.sum(neighbors[:, :, 0] * maska)
            result_array[i, j, 1] = np.sum(neighbors[:, :, 1] * maska)
            result_array[i, j, 2] = np.sum(neighbors[:, :, 2] * maska)

    # Tworzenie obrazka wynikowego na podstawie tablicy NumPy
    np.save("test1.npy", result_array)
    result_array = np.clip(result_array, 0, 255)
    np.save("test2.npy", result_array)
    result_img = Image.fromarray(result_array.astype(np.uint8))
    return result_img


def filtrRPSnp(Img, tryb):
    img_array = np.array(Img)
    w, h, _ = img_array.shape
    img_array = np.clip(img_array, 0, 255)
    if tryb == 0:
        maska = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, -1.0], [0.0, 0.0, 0.0]])
    elif tryb == 3:
        maska = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, -1.0, 0.0]])
    
    result_array = np.zeros_like(img_array)

    for i in range(1, w-1):
        for j in range(1, h-1):
            neighbors = img_array[i-1:i+2, j-1:j+2]
            print(neighbors)
            print(maska)
            result_array[i, j] = np.sum(neighbors * maska, axis=(0, 1))
            print(result_array[i, j])

    result_array = np.clip(result_array, 0, 255).astype(np.uint8)
    result_img = Image.fromarray(result_array)

    return result_img
                
                
def filtrRPS(Img, tryb):
    result_img = Image.new('RGB', Img.size)
    w, h = Img.size
    if tryb == 0:
        maska = [[0,0,0],[0,1,-1],[0,0,0]]
    elif tryb == 3:
        maska = [[0,0,0],[0,1,0],[0,-1,0]]
    elif tryb == 1:
        maska = [[1,1,1],[0,0,0],[-1,-1,-1]]
    elif tryb == 4:
        maska = [[1,0,-1],[1,0,-1],[1,0,-1]]
    elif tryb == 2:
        maska = [[1,2,1],[0,0,0],[-1,-2,-1]]
    elif tryb == 5:
        maska = [[1,0,-1],[2,0,-2],[1,0,-1]]
    elif tryb == 6:
        maska = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
        
        

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

def adjust_contrast(image, factor):
    img_array = np.array(image)

    mean_values = np.mean(img_array, axis=(0, 1))

    adjusted_array = (img_array - mean_values) * factor + mean_values

    adjusted_array = np.clip(adjusted_array, 0, 255)

    adjusted_image = Image.fromarray(adjusted_array.astype(np.uint8))

    return adjusted_image