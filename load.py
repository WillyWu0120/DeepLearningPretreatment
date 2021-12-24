import json
import glob
from os import path
import matplotlib.pyplot as plt


def folder_list():
    return glob.glob('Labels/*')


def image_list(folder):
    return glob.glob(f'{folder}/*.png')


def load_labels(folder):
    with open(path.join(folder, 'data.json'), 'r') as f:
        return json.load(f)


def load_image(image_path, label_list):
    image = plt.imread(image_path)
    image_id = path.splitext(path.basename(image_path))[0]
    label = [v for v in label_list if v["id"] == int(image_id)][0]
    print(image_id, label)
    return image, label


def load():
    folders = folder_list()
    data = []
    labels = []
    for folder in folders:
        print(folder)

        l = load_labels(folder)
        for image_path in image_list(folder):
            image, label = load_image(image_path, l)
            data.append(image)
            labels.append(label)

        print('-' * 50)

    print(len(data), len(labels))


if __name__ == '__main__':
    load()
