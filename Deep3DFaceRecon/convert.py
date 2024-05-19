from options.convert_options import ConvertOptions
import sys
import subprocess
import os
import shutil
import random
import string
from typing import List
import pymeshlab as ml


def random_letters_string(length: int):
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(length))


def load_data(from_path: str, to_path: str):
    if not os.path.exists(to_path):
        os.mkdir(to_path)

    for directory, subdirectories, files in os.walk(from_path):
        def filter_img(filename):
            return filename.endswith(".png") or filename.endswith(".jpg")

        images = list(filter(filter_img, files))

        if len(images) == 0:
            return FileNotFoundError('No images in input path!')

        for image in images:
            shutil.copyfile(os.path.join(from_path, image), os.path.join(to_path, image))

    return None


def call_algorithm(temp_folder_path: str):
    command = subprocess.Popen(
        ['python', 'test.py', '--name=face_recon_feat0.2_augment', '--epoch=20', f'--img_folder={temp_folder_path}',
         '--use_opengl=False', '--force_landmarks=True'])
    command.wait()
    print(command.stdout)
    pass


def transform(from_path: str, to_path: str):
    # https://pymeshlab.readthedocs.io/en/latest/

    for directory, subdirectories, files in os.walk(from_path):
        def filter_obj(filename):
            return filename.endswith(".obj")

        models = list(filter(filter_obj, files))
        ms = ml.MeshSet()

        for model in models:
            ms.load_new_mesh(os.path.join(from_path, model))
            ms.save_current_mesh(os.path.join(to_path, model[:len(model) - 4] + '.ply'), save_face_color=True)
            ms.clear()

    pass


def clean_up(temp_folders: List[str]):
    for path in temp_folders:
        print(path)
        shutil.rmtree(path)
    pass


if __name__ == '__main__':
    opt = ConvertOptions().parse()  # Get arguments
    if opt.input is None or opt.output is None:
        print("Can't work without input or output!")
        sys.exit()

    input_abs = os.path.abspath(opt.input)
    output_abs = os.path.abspath(opt.output)
    print(f"Input abs. path: {input_abs}")
    print(f"Output abs. path: {output_abs}")

    generated_key = random_letters_string(10)
    datasets = os.path.join('./datasets', generated_key)
    temp_output = os.path.join('./checkpoints/face_recon_feat0.2_augment/results', generated_key, 'epoch_20_000000')
    print(f'Temp folder is {datasets}')

    print('Loading data!')
    err = load_data(input_abs, datasets)
    if err is not None:
        print(f"Couldn't load data from {input_abs}: {err}")
        clean_up(datasets)
        sys.exit()

    call_algorithm(datasets)

    print('Converting output!')
    transform(temp_output, output_abs)
    load_data(temp_output, output_abs)

    print('Cleaning up!')
    clean_up([datasets, os.path.join('./checkpoints/face_recon_feat0.2_augment/results', generated_key)])
