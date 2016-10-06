from setuptools import setup


setup(
    name = 'prefixrun',
    version = '0.1.0',
    description = 'Sequentially run programs prefixed with <integer>-',
    long_description = open('README.md').read(),
    url = 'https://github.com/jakesherman/prefixrun',
    author = 'Jake Sherman',
    author_email = 'jake@jakesherman.com',
    license = 'MIT license',
    packages = ['prefixrun', 'prefixrun.utilities'],
    package_dir = {
        'prefixrun':'prefixrun',
        'prefixrun.utilities':'prefixrun/utilities'
    },
    entry_points = {
    'console_scripts': [
        'prefixrun = prefixrun.utilities.command_line:launch_new_instance',
        ]
    },
    install_requires = [
    'tabulate',
    ],
    zip_safe = False)
