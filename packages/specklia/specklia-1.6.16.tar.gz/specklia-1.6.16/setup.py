"""Setup file for The specklia client."""
import os

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if os.path.exists("full_version.txt"):
    with open("full_version.txt", "r", encoding="utf-8") as fh:
        """
        Note that this file is generated by the CI chain based on the git tag
        (by ew_continuous_integration/define_new_version_number.py)
        It should not be present in the repository by default.
        """
        version_number = fh.read()
else:
    version_number = 'v0.0.0'  # default value when under development

setup(
    name='specklia',
    version=version_number,
    description='Python client for Specklia, a geospatial point cloud database by Earthwave.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Earthwave Ltd',
    author_email='support@earthwave.co.uk',
    url='https://specklia.earthwave.co.uk/static/docs/index.html',
    python_requires=">=3.9",
    license='MIT',
    packages=find_packages(),
    # These generate the icons in the sidebar on PyPI
    project_urls={
        'Homepage': 'https://specklia.earthwave.co.uk/static/docs/index.html',
        'Changelog': 'https://specklia.earthwave.co.uk/static/docs/change_log.html',
        'Documentation': 'https://specklia.earthwave.co.uk/static/docs/index.html',
        'Twitter': 'https://twitter.com/earth__wave'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.9',
        'Topic :: Database :: Front-Ends',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Science/Research'
    ],
    # note requirements listed ininstall_requires should be the *minimum required*
    # in order to allow pip to resolve multiple installed packages properly.
    # requirements.txt should contain a specific known working version instead.
    install_requires=[
        'blosc',
        'flask',
        'geopandas',
        'pandas',
        'pyarrow',
        'rasterio',
        'requests',
        'shapely',
        'simple-websocket',
    ],
)
