import os
import subprocess
import shutil
import fileinput
import argparse

from typing import Dict, Any

def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='This script processes a RISC-V assembly file and generates an Uppaal model on which SMC queries are run.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        'query', type=str,
        help='Path to the query file for the experiment.'
    )

    parser.add_argument(
        '-m', '--model', type=str,
        help='The path to the Uppaal model.'
    )
    parser.add_argument(
        '-qo', '--query-output', type=str, default='./query.q',
        help='The proceeding path from the output at which the query file is saved.'
    )
    parser.add_argument(
        '-lo', '--log-output', type=str, default='./verifyta.log',
        help='The proceeding path from the output at which the log file is saved.'
    )

    return parser

def line_replacements(path: str, replacements: Dict[str, str]):
    with fileinput.input(path, inplace=True) as file:
        for line in file:
            for (key, value) in replacements.items():
                line = line.replace(key, value)
            # stdout is redirected to the file.
            # "end=''" avoids adding new lines to the end
            print(line, end='')

def run_verifyta(
    model_path: str, query_path: str,
    verifyta: str = 'verifyta',
    stdout: Any = None
) -> int:
    command = [
        verifyta, model_path, query_path,
        '--silence-progress', '--summary',
    ]

    if isinstance(stdout, str):
        with open(stdout, 'w') as file:
            return subprocess.run(command, stdout=file).returncode

    return subprocess.run(command, stdout=stdout).returncode

def replace_and_run(
    model: str, query: str,
    query_output: str, log_output: str,
    replacements: Dict[str, str],
):
    shutil.copy2(query, query_output)
    line_replacements(query_output, replacements)

    verifyta_process = run_verifyta(model, query_output, stdout=log_output)

    if verifyta_process != 0:
        print(f'ERROR: VerifyTA returned with error code: {verifyta_process}')
