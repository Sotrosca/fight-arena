from setuptools import find_packages, setup

setup(
    name="fight_arena",
    version="0.5",
    packages=find_packages(),
    py_modules=["game", "constants", "fighter", "layers"],
    install_requires=["pygame==2.5.2"],
)
