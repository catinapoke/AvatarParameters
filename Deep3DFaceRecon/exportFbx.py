import bpy
import sys
import ntpath


# Extracts file name from file path
def get_filename(path):
    path, name = ntpath.split(path)
    return name or ntpath.basename(path)


# Clears the scene
def delete_all():
    bpy.ops.object.delete({"selected_objects": [o for o in bpy.context.scene.objects]})


# Executes a py file
def exec_py_file(filepath):
    file = open(filepath)
    exec(file.read())


# Gets command line arguments
def get_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    return argv[0], argv[1]


# Obtain arguments
filepath, output_directory = get_args()

# Get the file name
filename = get_filename(filepath)

# Compose the fbx file name
output_filepath = ntpath.join(output_directory, filename + ".fbx")

# Clean the scene
delete_all()

# Run the py file
bpy.ops.import_mesh.ply(filepath=filepath)
# exec_py_file(filepath)
# import .ply from filepath

# Export to fbx
bpy.ops.export_scene.fbx(filepath=output_filepath, check_existing=False, use_selection=False, use_mesh_modifiers=True)
