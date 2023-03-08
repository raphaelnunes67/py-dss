import opendssdirect as dss

from tools import *


results = HandleFiles()

results.set_folder_in_results('new_folder')

print(results.get_folder_path_in_results())

results.remove_file('text.txt')

results.remove_folder()

