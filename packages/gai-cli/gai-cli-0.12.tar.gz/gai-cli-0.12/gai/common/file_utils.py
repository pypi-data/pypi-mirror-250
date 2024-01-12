import os

def this_dir(curr_dir, join_file):
    current_directory = os.path.dirname(os.path.abspath(curr_dir))
    return os.path.join(current_directory,join_file)
