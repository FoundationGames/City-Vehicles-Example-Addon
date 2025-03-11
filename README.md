# City Vehicles Example Addon for Automobility

A datapack and resource pack that can be installed alongside [Automobility](https://github.com/FoundationGames/Automobility/tree/1.21-rewrite) to add a few custom vehicle types (currently, five different-colored buses). <br/>
Intended to serve as an example and template for addon creators.

## Buildscript: `build.py`
This project includes a python buildscript to automatically generate the following:
- Resource Pack (.zip)
- Data Pack (.zip)
- Fabric/Neoforge Mod (.jar)
Run it with `python build.py`.

### Build Options: `project.txt`
- This file contains parameters for building the resource/data pack and mod jar.
- Edit them to fit the description of your own addon, should you use this as a template.

### Private Build Options: `workspace.txt`
- This file **is ignored by git**. You will not find it in this repository. Run the buildscript to create it.
- Build parameters in this file will work the same way as those in `project.txt`, however this file is meant for parameters relevant to your system only.
    - `build.assets.out=...`: Comma separated list of absolute filepaths to copy the resource pack to. Meant for quick testing and iteration.
    - `build.data.out=...`: Comma separated list of absolute filepaths to copy the data pack to. Meant for quick testing and iteration.
    - `build.mod.out=...`: Comma separated list of absolute filepaths to copy the mod jar to. Not the quickest way to iterate, but there if you need it.