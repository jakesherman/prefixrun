"""prefixrun.py - contains the class that does all of the work.
"""

import csv
import os
import subprocess
import tabulate
import time


class PrefixRun(object):
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

    PrefixRun will take those first 5 files, the ones with integer prefixes, and
    run them in order of those prefixes, so first 1-transfer_data.sh is run, 
    then 2-build_tables.hql, and so on until we finally run 
    5-visualize_present.R.

    A default set of file extensions / executions is contained in the 
    default_extensions method. 

    Examples -------------------------------------------------------------------

    Initializing a PrefixRun object:

    run = PrefixRun()  # -- using the current working directory by default

    Adding a custom extension (though .sh is already in the defaults):

    run = PrefixRun(custom_extensions = {'.sh' : ['bash']}) 

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
        self.directory = directory
        self.extensions = self.default_extensions()
        if custom_extensions is not None:
            for k, v in custom_extensions.items():
                self.extensions[k] = v


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
        want to run the file, and if so what order to run it in. Files starting
        with <int>- will be run, in order of the integer prefixes.
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
        """Identify which files to run, build a list of lists containing file
        orders, names, and NA values that will be filled in later.
        """
        files = os.listdir(self.directory)
        files_orders = [(self.should_we_run_this_file(f)[0], f) for f in files
                        if self.should_we_run_this_file(f)]
        orders = [x[0] for x in files_orders]
        if len(orders) != len(set(orders)):
            raise Exception('One or more files have the same integer prefix')
        file_data = []
        for order, file_name in sorted(files_orders, key = lambda x: x[0]):
            file_data.append([order, file_name, 'NA', 'NA', 'NA', 'No'])
        self.file_data = file_data
        return None


    def run_file(self, file_name):
        """Runs a file name, using its extension to determine how to run it.
        """
        filename, file_extension = os.path.splitext(file_name)
        call = self.extensions[file_extension] + [file_name]
        subprocess.call(call)
        return None


    def run_files(self):
        """Runs a list of files, saving data about timing and whether the files
        ran as it happens.
        """

        for index, file_name in enumerate([x[1] for x in self.file_data]):
            start, start_time = time.time(), time.strftime('%c')
            ran_successfully = True
            try:
                self.run_file(file_name)
            except:
                ran_successfully = False
            finally:
                end, end_time = time.time(), time.strftime('%c')
                elapsed = (end - start) / 60
                #self.file_data[index][]
            if not ran_successfully:
                break
        return None