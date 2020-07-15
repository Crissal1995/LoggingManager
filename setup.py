import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

MAJOR, MINOR, MICRO = 0, 1, 0
VERSION = '{}.{}.{}'.format(MAJOR, MINOR, MICRO)

metadata = dict(
    name='LoggingManager',
    author='Cristiano Salerno',
    author_email='cristianosalerno1@gmail.com',
    url='https://github.com/Crissal1995/LoggingManager',

    description='A simple wrapper around logging module.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    version=VERSION,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

setuptools.setup(**metadata)
