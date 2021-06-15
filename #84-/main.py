from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt


def water_mark_image(image_path: str):
    image = Image.open(image_path)
    image_array = np.array(image)
    length, width = image_array.shape[0], image_array.shape[1]
    extension = np.array([[[0, 0, 0, 255] for _ in range(width)] for _ in range(length//10)])
    font = ImageFont.truetype("Ramaraja-Regular.ttf", 32)
    temp_image_array = np.concatenate((image_array, extension), axis=0)
    temp_image = Image.fromarray(temp_image_array.astype(np.uint8))
    draw = ImageDraw.Draw(temp_image)
    draw.text((width//10, length + length//50), 'THE POOP HATH COME FOR YE',
              (255, 255, 255), font=font)
    temp_image.save('new.png')
    marked_image_array = np.array(temp_image)
    return marked_image_array


new_img = water_mark_image('r.png')
plt.imshow(new_img)
plt.show()
