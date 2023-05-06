import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def histogram(image):
    # Konwertuj obrazek do tablicy NumPy
    img_array = np.array(image)

    # Wygeneruj histogram dla każdej składowej koloru
    hist_r, bins_r = np.histogram(img_array[:, :, 0].ravel(), bins=256, range=(0, 255))
    hist_g, bins_g = np.histogram(img_array[:, :, 1].ravel(), bins=256, range=(0, 255))
    hist_b, bins_b = np.histogram(img_array[:, :, 2].ravel(), bins=256, range=(0, 255))

    # Wyświetl histogram
    plt.figure(figsize=(8, 6))
    plt.plot(bins_r[:-1], hist_r, color='red', alpha=0.5, label='Red')
    plt.plot(bins_g[:-1], hist_g, color='green', alpha=0.5, label='Green')
    plt.plot(bins_b[:-1], hist_b, color='blue', alpha=0.5, label='Blue')
    plt.title('Histogram R, G, B')
    plt.xlabel('Wartość piksela')
    plt.ylabel('Liczba pikseli')
    plt.legend()

    # Konwersja histogramu na obiekt klasy PIL.Image
    fig = plt.gcf()
    fig.canvas.draw()
    hist_img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    return hist_img