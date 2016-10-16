from setuptools import setup


setup(
    name = 'runningshoes',
    version = '0.1.0',
    description = 'Sequentially run programs prefixed with <integer>-',
    long_description = open('README.md').read(),
    url = 'https://github.com/jakesherman/runningshoes',
    author = 'Jake Sherman',
    author_email = 'jake@jakesherman.com',
    license = 'MIT license',
    packages = ['runningshoes', 'runningshoes.utilities'],
    package_dir = {
        'runningshoes':'runningshoes',
        'runningshoes.utilities':'runningshoes/utilities'
    },
    entry_points = {
    'console_scripts': [
        'runningshoes = runningshoes.utilities.command_line:launch_new_instance',
        ]
    },
    install_requires = [
        'pandas',
        'tabulate',
    ],
    zip_safe = False)
