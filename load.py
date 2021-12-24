import json
import glob
from os import path


def folder_list():
    return glob.glob('Labels/*')


def image_list(folder):
    return glob.glob(f'{folder}/*.png')


def load_labels(folder):
    with open(path.join(folder, 'data.json'), 'r') as f:
        return json.load(f)


def load():
    folders = folder_list()
    data = []
    labels = []
    for folder in folders:
        print(folder)

        images = image_list(folder)
        l = load_labels(folder)
        print(len(images), len(l), len(images) == len(l))

        print('-' * 50)


if __name__ == '__main__':
    load()
