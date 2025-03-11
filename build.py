import shutil
import zipfile
import os
import re

def build(vars: dict):
    print("Starting Build...")

    build_mc_pack(vars, "assets")
    build_mc_pack(vars, "data")
    build_mod(vars)

    print("Finished!")

# --------------------------------------

def build_mc_pack(vars: dict, name: str):
    namespace = vars["namespace"]
    resource_folder = vars[f"build.{name}"]
    meta_file = vars[f"build.{name}.meta"]
    icon_file = vars["build.icon"]
    license_file = vars["build.license"]
    filename = sub_vars(vars, vars[f"build.{name}.file"])
    output_dirs = get_out_dirs(vars, f"build.{name}.out")

    print(f"Building Pack '{resource_folder}'")

    output_dir = output_dirs[0]
    zipfile_name = f"{filename}.zip"
    zipfile_path = os.path.join(output_dir, zipfile_name)
    
    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as packfile:
        for root, _, files in os.walk(resource_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipped_path = os.path.join(resource_folder, os.path.relpath(file_path, resource_folder))
                packfile.write(file_path, zipped_path)
        
        with open(meta_file, "r") as mf:
            contents = "".join(mf.readlines())
            packfile.writestr("pack.mcmeta", sub_vars(vars, contents))
        
        if os.path.exists(icon_file):
            packfile.write(icon_file, "pack.png")
        
        if os.path.exists(license_file):
            packfile.write(license_file, license_file + f"_{namespace}")

    copy_to_out_dirs(zipfile_path, zipfile_name, output_dirs)    

def build_mod(vars: dict):
    namespace = vars["namespace"]
    resource_folders = vars["build.mod.resources"].split(",")
    manifest_mappings = vars["build.mod.manifest"].split(",")
    meta_file = vars["build.mod.meta"]
    icon_file = vars["build.icon"]
    license_file = vars["build.license"]
    filename = sub_vars(vars, vars["build.mod.file"])
    output_dirs = get_out_dirs(vars, "build.mod.out")

    print(f"Building Fabric/NeoForge Mod")

    output_dir = output_dirs[0]
    jarfile_name = f"{filename}.jar"
    jarfile_path = os.path.join(output_dir, jarfile_name)
    
    with zipfile.ZipFile(jarfile_path, 'w', zipfile.ZIP_DEFLATED) as packfile:
        for resource_folder in resource_folders:
            for root, _, files in os.walk(resource_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipped_path = os.path.join(resource_folder, os.path.relpath(file_path, resource_folder))
                    packfile.write(file_path, zipped_path)
        
        for manifest_mapping in manifest_mappings:
            kv: list = manifest_mapping.split(":")
            if len(kv) >= 1:
                kv.append(kv[0])
            else:
                continue

            manifest_file = kv[0]
            zipped_manifest_file = kv[1]

            with open(manifest_file, "r") as mf:
                contents = "".join(mf.readlines())
                packfile.writestr(zipped_manifest_file, sub_vars(vars, contents))
        
        with open(meta_file, "r") as mf:
            contents = "".join(mf.readlines())
            packfile.writestr("pack.mcmeta", sub_vars(vars, contents))
        
        if os.path.exists(icon_file):
            packfile.write(icon_file, f"{namespace}.png")
        
        if os.path.exists(license_file):
            packfile.write(license_file, license_file + f"_{namespace}")

    copy_to_out_dirs(jarfile_path, jarfile_name, output_dirs)    

def prepare_build_dir():
    if not os.path.exists("./build/"):
        os.makedirs("./build/")

def read_vars(vars: dict, path: str):
    with open(path, "r") as f:
        lines = f.readlines()

        for l in lines:
            if l.startswith("#"):
                continue

            kv = re.split(r"(\s*=\s*)", l)
            if len(kv) >= 3:
                vars[kv[0]] = kv[2].strip("\n")

def sub_vars(vars: dict, content: str) -> str:
    out = content
    for k in vars:
        out = out.replace("${" + k + "}", vars[k])
    return out

def get_out_dirs(vars: dict, key: str) -> list:
    outs = ["build"]
    try:
        v = vars[key]
    except KeyError:
        return outs

    if len(v) > 0:
        for p in v.split(","):
            outs.append(p)
    
    return outs

def copy_to_out_dirs(zipfile_path, zipfile_name, output_dirs):
    if len(output_dirs) > 1:
        for dir in output_dirs[1:]:
            shutil.copy(zipfile_path, os.path.join(dir, zipfile_name))

if __name__ == "__main__":
    vars = {}

    try:
        with open("./workspace.txt", "x") as f:
            f.write("# Workspace-only variables\n")
    except FileExistsError:
        pass

    read_vars(vars, "./project.txt")
    read_vars(vars, "./workspace.txt")

    prepare_build_dir()
    build(vars)
