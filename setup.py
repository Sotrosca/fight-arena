import glob

from setuptools import find_packages, setup

setup(
    name="fight_arena",
    version="0.14",
    packages=find_packages(),
    py_modules=["game", "constants", "fighter", "layers", "components"],
    data_files=[(".", glob.glob("*.jpg"))],
    install_requires=["pygame==2.5.2"],
)
