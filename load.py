import json
import glob
from os import path
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

SHAPE = (50, 100)


def folder_list():
    return glob.glob('Labels/*')


def image_list(folder):
    return glob.glob(f'{folder}/*.png')


def load_labels(folder):
    with open(path.join(folder, 'data.json'), 'r') as f:
        return json.load(f)


def load_image(image_path, label_list):
    image = Image.open(image_path)
    image = image.resize(SHAPE)
    image_id = path.splitext(path.basename(image_path))[0]
    label = [v for v in label_list if v["id"] == int(image_id)][0]
    print(image_id, label)
    return np.array(image), label


def load():
    folders = folder_list()
    images = []
    pitch = []
    duration = []
    dots = []
    accidental = []
    for folder in folders:
        print(folder)

        l = load_labels(folder)
        for image_path in image_list(folder):
            image, label = load_image(image_path, l)
            print(image.shape)
            images.append(image)
            pitch.append(label['pitch'])
            duration.append(label['duration'])
            dots.append(label['dots'])
            accidental.append(label['accidental'])

        print('-' * 50)

    print(len(images), len(pitch))
    return {
        "images": np.array(images),
        "pitch": np.array(pitch, dtype=np.int32),
        "duration": np.array(duration, dtype=np.float32),
        "dots": np.array(dots, dtype=np.uint8),
        "accidental": np.array(accidental, dtype=np.uint8),
    }


def save(data):
    np.savez_compressed('data.npz', **data)


def hist(data):
    for key, value in data.items():
        if key == 'images':
            continue
        print(key, value)
        plt.figure()
        plt.title(key)
        plt.hist(value)
    plt.show()


if __name__ == '__main__':
    data = load()
    print(data['images'].shape)
    hist(data)
    # save(data)
