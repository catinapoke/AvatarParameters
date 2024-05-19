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
output_filepath = ntpath.join(output_directory, filename[:filename.rfind(".")] + ".fbx")

# Clean the scene
delete_all()

# Run the py file
bpy.ops.import_mesh.ply(filepath=filepath)
# exec_py_file(filepath)
# import .ply from filepath
for mesh in bpy.data.meshes: # https://docs.blender.org/api/current/bpy.types.Mesh.html
    if len(mesh.vertex_colors.values()) > 0:
        print(dir(mesh.vertex_colors[0]))
    if len(mesh.vertices.values()) > 0:
        print(dir(mesh.vertices[0]))
    break
    pass

# Export to fbx
# bpy.ops.export_scene.fbx(filepath=output_filepath, check_existing=False, use_selection=False, use_mesh_modifiers=True)
