from pathlib import Path
from django.contrib.sessions.backends import file
from setuptools import find_packages, setup

PACKAGE_NAME = "netbox_plugin_buildingplan"

def get_version():
    version_file = Path(file).parent / PACKAGE_NAME.replace("-", "_") / "version.py"
    with version_file.open() as f:
        for line in f.readlines():
            if "version" not in line:
                continue
            delimiter = "'" if "'" in line else '"'
            return line.split(delimiter)[1]
    raise RuntimeError("Could not find the version number")

setup(
    name=PACKAGE_NAME,
    version=get_version(),
    description="A NetBox plugin to add building plans to tenants.",
    author="Ledy Gaga",
    license="MIT",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)