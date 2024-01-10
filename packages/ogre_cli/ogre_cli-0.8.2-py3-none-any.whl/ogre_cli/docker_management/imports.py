import ast
import glob
import os
import subprocess

from isort import place_module

from .constants import ALTERNATIVE_MODULE_NAMES
from .utilities import extension, list_python_files, listdirs

# Adapted from:
#
# https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script
#
# and
#
# https://stackoverflow.com/questions/6463918/how-to-get-a-list-of-all-the-python-standard-library-modules


class GetImports:
    def __init__(self, project_path):
        self.modules = set()
        self.project_path = project_path
        self.ipynbfiles = []
        self.folders_in_project_path = listdirs(self.project_path)
        self.files_in_project_path = list_python_files(self.project_path)

    def visit_Import(self, node):
        for name in node.names:
            self.modules.add(name.name.split(".")[0])

    def visit_ImportFrom(self, node):
        # if node.module is missing it's a "from . import ..." statement
        # if level > 0 it's a "from .submodule import ..." statement
        if node.module is not None and node.level == 0:
            self.modules.add(node.module.split(".")[0])

    def comes_with_repo(self, module_name):
        """
        Tell if input module comes with the repo, i.e., it is a custom module
        implemented in the repo.

        It compares module_name against a list of folders and a list of files present in
        the repo.

        If a module_name comes with repo, then the module is omitted from requirements.txt
        file.
        """

        res = False
        if module_name in self.folders_in_project_path or module_name in self.files_in_project_path:
            res = True

        return res

    @staticmethod
    def is_native_module(module_name):
        """
        Tell if input module is native to system's python version.

        Returns True string if module is part of stdlib, False otherwise.
        """
        res = False
        if place_module(module_name) == "STDLIB":
            res = True
        return res

    @staticmethod
    def get_alternative_name(module_name):
        """
        Some modules are imported using a namespace different from its original one.
        For example, to call module opencv-python, we need to import namespace 'cv2'.

        This function allows for writing the right namespace in the requirements file,
        avoiding breaking the module installation during docker build.

        It works by consulting a list of alternative names.
        """
        res = module_name
        if module_name in ALTERNATIVE_MODULE_NAMES.keys():
            res = ALTERNATIVE_MODULE_NAMES[module_name]
        return res

    def ipynb_to_py(self):
        """
        Convert ipynb files (jupyter notebooks) to python scripts.

        This enables us to extract the modules imported by jupyter notebooks.
        """
        pattern_ipynb = glob.glob(
            os.path.join("{}".format(self.project_path), "**/", "*.ipynb"),
            recursive=True,
        )

        print(pattern_ipynb)

        for filename in pattern_ipynb:
            print(filename)
            # subprocess to convert notebook to python
            convert_cmd = 'jupyter nbconvert --to python "{}"'.format(filename)
            p = subprocess.Popen(convert_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = p.communicate()
            p_status = p.wait()

            filename_py = filename[:-5] + "py"
            self.ipynbfiles.append(filename_py)
        print("ipynb files")
        print(self.ipynbfiles)

    def get_py_files(self):

        pattern_py = glob.glob(
            os.path.join("{}".format(self.project_path), "**/", "*.py"), recursive=True
        )
        pyfiles = []

        for filename in pattern_py:
            pyfiles.append(filename)

        return pyfiles

    def remove_converted_ipynb_files(self):
        """
        Remove the py files created from ipynb. We only need them to create the
        requirements.txt file.
        """

        for filename in self.ipynbfiles:
            os.remove(filename)

    def get_imported_modules(self):
        """
        Get all the modules imported inside filename.
        """
        node_iter = ast.NodeVisitor()
        node_iter.visit_Import = self.visit_Import
        node_iter.visit_ImportFrom = self.visit_ImportFrom

        pyfiles = self.get_py_files()
        print("pyfiles = {}".format(pyfiles))

        for filename in pyfiles:
            with open(filename) as f:
                node_iter.visit(ast.parse(f.read()))
            # print("{}: {}".format(filename, self.modules))
