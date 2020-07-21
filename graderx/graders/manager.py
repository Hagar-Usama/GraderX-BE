from werkzeug.datastructures import FileStorage
from pathlib import Path
import shlex
import subprocess
import os
## dependencies for docker
import patoolib
import glob
import shutil
# pip install patool


def clean_directory(dir):
    files = dir.glob('*')
    for f in files:
        if f.is_dir():
            shutil.rmtree(str(f))
        else:
            f.unlink()

def extract_file(file_path, verbosity=-1):
    patoolib.extract_archive(file_path, outdir=file_path.parent, verbosity=verbosity)
    os.remove(file_path)
    return True

def extract_submissions(dest_directory: Path, submissions_file: FileStorage,  verbosity= 0):
    """
    Args:
    dest_directory: Path. Submission directory found in [lab_name]/config.py
    submissions_file: FileStorage. It is used by the request object to represent uploaded files. 
 
    Returns: bool
    status: True on sucessful extraction

    Actions:
    extracts the submissions file in the destenation directory and removes the rar (or Whatever) file

    """
    
    file_name = submissions_file.filename
    # clean the submissions directory, if it doesn't exist create it along with missing parents
    if dest_directory.exists():
        clean_directory(dest_directory)
    else:
        dest_directory.mkdir(parents=True)

    submissions_file.save(dst=(dest_directory / file_name))
    file_path = dest_directory.joinpath(file_name)
    # check if exists
    try:
        status = [extract_file(file_path), False][os.path.exists(file_path)]
        print("***[Success]: File extracted successfully")
    except:
        print("***[Error]: Archive is damaged")
        return False
    return status



def run_grader_commands(lab_id):
    curr_dir = str(Path(__file__).parent.resolve())
    cmd = shlex.split(f"pytest -vv --tb=short --show-capture=no {curr_dir}/courses/cc451/app/{lab_id}/test_run_grader.py")
    file_name = "output.txt"
    with open(file_name, "w+") as f:
        subprocess.run(cmd, stdout=f)
    parser_file = "parser_output"
    lab_number = lab_id.split('lab')[-1]
    with open(file_name, "r") as fi:
        with open(parser_file, "w+") as fo:
            cmd = shlex.split(f"python {curr_dir}/courses/cc451/app/lib/console_log_parser.py {lab_number} {curr_dir}/courses/cc451/app/res/{lab_id}")
            subprocess.run(cmd, stdin=fi, stdout=fo)


def run_grader(lab_id: str, submissions_file: FileStorage) -> dict:
    curr_dir = str(Path(__file__).parent.resolve())
    extract_submissions(Path(f"{curr_dir}/courses/cc451/app/{lab_id}/submissions/2020"), submissions_file)
    run_grader_commands(lab_id)
    return True
    