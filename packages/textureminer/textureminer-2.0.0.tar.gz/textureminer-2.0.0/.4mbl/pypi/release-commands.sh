exit 0 #! this is a shell file because syntax highlighting is nice, but it's not meant to be run as a script

#! DO THE SAME STEPTS FIRST WITH AN ALPHA VERSION, THEN FULL RELEASE

# install/upgrade utils
py -m pip install --upgrade pip pipreqs build twine

# update reqs
py -m pipreqs.pipreqs . --force

# build
py -m build

# install from file
pip uninstall textureminer -y && pip install ./dist/textureminer-<VERSION_NUMBER>-py3-none-any.whl

#! DANGER ZONE: upload to pypi
py -m twine upload -u __token__ -p $(cat ./.4mbl/pypi/token.txt) dist/*

# install from pypi and test
py -m venv venv/testing_textureminer && venv/testing_textureminer/Scripts/activate && py -m pip install --upgrade textureminer
textureminer -v && textureminer --help
rmrf venv/testing_textureminer
