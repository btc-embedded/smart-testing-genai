import json
import os
import sys

import git

# BTC EmbeddedPlatform hook script for architecture update check and traceability data
# 
# Called by BTC EmbeddedPlatform when the following events occur:
# - Architecture update check: before architecture update
# - ARCHITECTURE_META_INFO: during architecture import or update
# - REQUIREMENT_META_INFO: during requirement import or update
# - TESTING_META_INFO: during load/save of the test project
# 
# A preference controls the command that is executed when the trigger events described above occur:
# <preference
#   name="GENERAL_HOOKS_COMMAND"
#   value="python C:/ProgramData/BTC/ep/hooks/btc_hooks.py" />

# architecture update check
ARCHITECTURE_UPDATE_NEEDED = "ARCH_UPDATE_NEEDED"
# traceability hooks
ARCHITECTURE_META_INFO = "ARCH_ADD_META_INFO"
REQUIREMENT_META_INFO = "REQ_ADD_META_INFO"
TESTING_META_INFO = "EP_ADD_META_INFO"

def main(input_data) -> dict:
    use_case = input_data["useCase"]
    meta_data = input_data.get("metaData", {})
    return_data = {}
    
    if use_case == ARCHITECTURE_META_INFO:
        return_data["metaData"] = collect_architecture_metadata(meta_data)
    elif use_case == TESTING_META_INFO:
        return_data["metaData"] = collect_testing_metadata(meta_data)
    
    return return_data


def collect_architecture_metadata(meta_data) -> dict:
    arch_metadata = {}
    if meta_data and 'BTC EmbeddedPlatform' in meta_data:
        meta_data = meta_data['BTC EmbeddedPlatform']
        model_path = meta_data['Simulink']['Model File']

        arch_metadata['Last change (Model)'] = get_last_change(model_path)
        tldd_path = model_path[:-4] + '.dd'
        if os.path.isfile(tldd_path):
            arch_metadata['Last change (DD)'] = get_last_change(tldd_path)

    return arch_metadata


def collect_testing_metadata(meta_data) -> dict:
    tst_metadata = {}
    if meta_data and 'BTC EmbeddedPlatform' in meta_data:
        meta_data = meta_data['BTC EmbeddedPlatform']
        epx_file = meta_data['Profile Path']
        tst_metadata['Last change (Test Project)'] = get_last_change(epx_file)
    return tst_metadata


# -----------------
# Helper functions
# -----------------

def get_last_change(file_path) -> str:
    """
    Retrieves the last commit information for a given file in a Git repository.

    Args:
        file_path (str): The path to the file for which to retrieve the last commit information.

    Returns:
        str: A string containing the date and time of the last commit, the author's name, 
             the commit message, and the first 8 characters of the commit hash. 
             If no commit is found, returns an empty string.
    """
    repo = git.Repo(os.path.dirname(file_path), search_parent_directories=True)
    repo_root = repo.git.rev_parse("--show-toplevel")
    file_path_in_repo = os.path.relpath(file_path, repo_root)
    last_commit = next(repo.iter_commits(paths=file_path_in_repo, max_count=1), None)
    if last_commit:
        return f"[{last_commit.committed_datetime}] {last_commit.author.name}: {last_commit.message.strip()} (hash: {last_commit.hexsha[:8]})"

    
if __name__ == '__main__':
    # expecting two arguments: the path to the input file (json) and the path to the output file (json)
    if len(sys.argv) == 3 and os.path.isfile(sys.argv[1]):
        # (1) read input data from file
        input_data_file = sys.argv[1]
        with open(input_data_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        # (2) call main function
        return_data = main(input_data)
        
        # (3) write return data to file
        output_data_file = sys.argv[2]
        with open(output_data_file, 'w') as f:
            f.write(json.dumps(return_data, indent=4))

    # handling invalid calls
    elif not os.path.isfile(sys.argv[1]):
        print(f"File not found: {sys.argv[1]}")
        exit(1)
    else:
        print("Usage: btc_hooks.py <input_file> <output_file> (.json)")
        exit(1)
        