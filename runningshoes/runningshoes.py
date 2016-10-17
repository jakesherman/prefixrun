from __future__ import division, print_function

"""runningshoes.py - RunningShoes class.
"""

import csv
import os
import subprocess
from tabulate import tabulate
import time


class RunningShoes(object):
    """Run all of the files in a directory with a prefix of <integer>- in the
    order of their integer prefixes. This is a simple, straightforward way to
    create data analysis pipelines. For example, imagine that we have a
    directory with the following files:

    1-transfer_data.sh
    2-build_tables.hql
    3-pull_ingest.py
    4-model.py
    5-visualize_present.R
    myproject.py
    random.txt
    image.jpeg

    RunningShoes will take those first 5 files, the ones with integer prefixes,
    and run them in order of those prefixes, so first 1-transfer_data.sh is run,
    then 2-build_tables.hql, and so on until we finally run
    5-visualize_present.R.

    A default set of file extensions / executions is contained in the
    default_extensions method.

    Examples -------------------------------------------------------------------

    Initializing a RunningShoes object:

    run = RunningShoes()  # -- using the current working directory by default

    Adding a custom extension (though .sh is already in the defaults):

    run = RunningShoes(custom_extensions = {'.sh' : ['bash']})

    Seeing what extensions are available:

    print run.default_extensions()  # -- see the defaults
    print run.extensions()  # -- see the defaults + any custom extensions
    """


    def __init__(self, directory = os.getcwd(), custom_extensions = None):
        """Initialize a RunFiles object, setting up all of the necessary
        variables. Custom extensions will overwrite the default extensions with
        the same key.

        Parameters
        ----------
        directory : string (default is the current working directory)
            the directory to run files in

        custom_extensions: dict
            Keys are extensions (ex. .'sh') and values are the terminal commands
            to run those programs (ex. ['bash']) contained in lists. Defaults
            are provided in the default_extensions method. Any
        """
        self.directory = self.ensure_trailing_slash(directory)
        self.files = self.identify_files()
        self.extensions = self.default_extensions()
        if custom_extensions is not None:
            for k, v in custom_extensions.items():
                self.extensions[k] = v
        self.file_data = {
            'info': {},
            'meta': {
                'files': self.files,
                'initialized': time.strftime('%c')
            }
        }


    @staticmethod
    def ensure_trailing_slash(directory):
        """Ensure a trailing slash in a directory location.
        """
        if directory[-1] != '/':
            directory = directory + '/'
        return directory


    @staticmethod
    def default_extensions():
        """Where we define the default extensions. 'extensions' maps file
        extensions with commands used to execute files with that extension.
        """
        return {
            '.hql' : ['hive', '-f'],
            '.py' : ['python'],
            '.R' : ['Rscript'],
            '.scala': ['scala'],
            '.sh' : ['bash']
        }


    @staticmethod
    def should_we_run_this_file(file_name):
        """Given the string for a file name, determines 1. whether or not to we
        want to run the file, and 2. if so, what order to run it in.
        """
        parts = file_name.split('-')
        if len(parts) < 2:
            return False
        try:
            int(parts[0])
        except:
            return False
        return (True, int(parts[0]))


    def identify_files(self):
        """Identify which files to run, create a list of files to run in the
        order which they should be run in.
        """
        files = os.listdir(self.directory)
        files_orders = sorted([[self.should_we_run_this_file(f)[1], f] for f
                               in files if self.should_we_run_this_file(f)])
        orders, files = zip(*files_orders)
        if len(orders) != len(set(orders)):
            raise Exception('One or more files have the same integer prefix!')
        return files


    def run_file(self, file_name):
        """Runs a file, using its extension to determine how to run it.
        """
        filename, file_extension = os.path.splitext(file_name)
        call = self.extensions[file_extension] + [file_name]
        subprocess.call(call)
        return None


    def run_files(self):
        """Runs many files, recording information on when the files were run,
        how long they took, and whether or not they ran successfully.
        """
        for order, file in enumerate(self.files, start = 1):
            start = time.time()
            self.file_data['info'][file] = {
                'ran': True,
                'start_time': time.strftime('%c')
            }
            try:
                self.run_file(self.directory + file)
                self.file_data['info'][file]['end_time'] = time.strftime('%c')
                self.file_data['info'][file]['elapsed'] = \
                    (time.time() - start) / 60
            except:
                self.file_data['info'][file]['end_time'] = time.strftime('%c')
                self.file_data['info'][file]['elapsed'] = \
                    (time.time() - start) / 60
                self.file_data['info'][file]['ran'] = False
                raise
        return None


    def format_file_data(self):
        """Formats a file_data dictionary into list of lists that can be nicely
        printed using the tabulate package.
        """
        results = []
        success_string = {
            True: 'Success',
            False: 'Failure'}
        for order, file in enumerate(self.files, start = 1):
            if self.file_data['info'].get(file, None) is not None:
                start_time = self.file_data['info'][file]['start_time']
                end_time = self.file_data['info'][file]['end_time']
                elapsed = self.file_data['info'][file]['elapsed']
                ran = self.file_data['info'][file]['ran']
                results.append([order, file, start_time, end_time, elapsed,
                    success_string[ran]])
            else:
                results.append([order, file, 'NA', 'NA', 'NA', 'NA'])
        return results


    def pretty_file_data(self):
        """Pretty version of file_data to be printed out.
        """
        headers = ['Order', 'File name', 'Start time', 'End time',
                   'Time elapsed (mins)', 'Status']
        return tabulate(self.format_file_data(), headers = headers,
            tablefmt = 'psql')


    def __str__(self):
        return self.pretty_file_data()


    __repr__ = __str__


    def run(self):
        """Run all of the files! This is the worker method for the whole class.
        """
        try:
            self.run_files()
        finally:
            print(self.pretty_file_data())
        return None
