import argparse
import os
import subprocess


def convert_ply_model_with_blender(blender_path: str, model_path: str):
    blender_script_path = os.path.dirname(__file__) + '\\exportFbx.py'  # exportFbx.py
    output_dir = os.path.dirname(model_path)

    # "<your path to blender>\blender.exe" --background --python exportFbx.py -- "$filename" "<your output directory>"
    # print(f'{blender_path} --background --python {blender_script_path} -- {model_path} {output_dir}')
    command = subprocess.Popen(
        [blender_path, '--background', '--python', blender_script_path, '--', model_path, output_dir])
    command.wait()
    pass


def convert_all_ply_to_fbx(input_path: str, blender_path: str):
    origin = os.path.abspath(input_path)
    for directory, subdirectories, files in os.walk(origin):
        def filter_obj(filename):
            return filename.endswith(".ply")

        models = list(filter(filter_obj, files))

        for model in models:
            model_path = os.path.join(origin, directory, model)
            convert_ply_model_with_blender(blender_path, model_path)
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        required=True,
                        metavar='PATH',
                        dest='input',
                        type=str,
                        help='Input/output images folder')
    parser.add_argument('-b', '--blender',
                        required=True,
                        metavar='PATH',
                        dest='blender',
                        type=str,
                        help='Blender.exe path')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    convert_all_ply_to_fbx(args.input, args.blender)
