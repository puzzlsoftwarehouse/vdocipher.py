from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='vdocipher.py',
    version='0.5.1',
    url='https://github.com/puzzlsoftwarehouse/vdocipher.py',
    license='MIT License',
    author='Puzzl Software House',
    author_email='hello@puzzl.com.br',
    keywords='vdocipher video api python wrapper',
    description='Just a VdoCipher api wrapper for python.',
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(),
)

install_requires = [
    'dataclasses-json',
    'requests_toolbelt'
]

extras_require = {
    'dev': [
        'pytest',
        'twine',
        'wheel'
    ]
}

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, extras_require=extras_require)
