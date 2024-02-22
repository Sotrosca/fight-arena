from setuptools import find_packages, setup

setup(
    name="fight_arena",
    version="0.8",
    packages=find_packages(),
    py_modules=["game", "constants", "fighter", "layers", "components"],
    package_data={"fight_arena": ["*.png", "*.jpg"]},
    install_requires=["pygame==2.5.2"],
)
