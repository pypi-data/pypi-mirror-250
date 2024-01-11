exit 0 #! this is a shell file because syntax highlighting is nice, but it's not meant to be run as a script

# install/upgrade utils
py -m pip install --upgrade pip pipreqs build twine

# update reqs
py -m pipreqs.pipreqs . --force

# build
py -m build

# install from file
pip uninstall textureminer -y && pip install ./dist/textureminer-0.0.0-py3-none-any.whl

# install from pypi
rmrf venv/testing_textureminer && py -m venv venv/testing_textureminer && venv/testing_textureminer/Scripts/activate && py -m pip install --upgrade textureminer





# venv testing
py -m venv venv/testing_textureminer && venv/testing_textureminer/Scripts/activate


# single line (assumes venv is already active)
py -m pip install --upgrade pip pipreqs build twine && py -m pipreqs.pipreqs . --force && py -m build && pip uninstall textureminer -y && pip install ./dist/textureminer-0.0.0-py3-none-any.whl && textureminer -v && textureminer --help
