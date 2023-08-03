#!/usr/bin/python3
from ftplib import FTP
from typing import List, Dict, Any, Union
import random
import string
import os
import glob
import argparse
from time import sleep

def generate_random_word() -> str:
    """
    Generates a random word
    """
    word :str = ''
    word_len = random.randint(7, 14)
    for _ in range(word_len):
        word += random.choice(string.ascii_letters)
    return ''.join(word)

def get_list_of_artifacts(artifacts_dir: str) -> List[str]:
    artifacts: List[str] = []
    for filename in glob.iglob(os.path.join(artifacts_dir, "**"), recursive=True):
        if os.path.isfile(filename):
            artifacts.append(filename)
    return artifacts

def parse_arguments(args: Union[str, None] = None) -> Dict[str, Any]:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Select random files from artifact directory and upload them to ftp server"
    )
    parser.add_argument(
        "-a",
        "--artifacts",
        type=str,
        default="artifacts",
        help="Directory of artifacts to upload",
    )
    parser.add_argument(
        "-f",
        "--ftp-server",
        type=str,
        default="ftp01",
        help="Hostname or ip of the FTP server",
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="Administrator",
        help="Username of the FTP server",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default="lab",
        help="Password of the FTP server",
    )
    parser.add_argument("-n", "--number-of-files", type=int, default=100, help="Number of files to upload")
    parser.add_argument("--min-sleep", type=int, default=3, help="Min time to wait between uploads")
    parser.add_argument("--max-sleep", type=int, default=5, help="Max time to wait between uploads")
    return vars(parser.parse_args(args))


def upload(args: Dict[str, Any]) -> None:
    """
    Upload number of files specified
    """
    # Connect to the FTP server
    with FTP(args['ftp_server']) as ftp:
        ftp.login(args['user'], args['password'])
        for _ in range(args['number_of_files']):
            file_path = random.choice(args['artifacts'])
            file_name = os.path.basename(file_path)
            name, extension = os.path.splitext(file_name)
            new_name = generate_random_word()
            new_name += extension
            command = f'STOR {new_name}'
            with open(file_path, 'rb') as file_hd:
                ftp.storbinary(command, file_hd)
                pass
            sleep_time = random.randint(args['min_sleep'],args['max_sleep'])
            print(f"Uploaded {file_path} as {new_name}, waiting {sleep_time} seconds")
            sleep(sleep_time)

def main() -> None:
    """
    Main function to read command line arguments and upload files
    """
    args = parse_arguments()
    artifacts = get_list_of_artifacts(artifacts_dir=args['artifacts'])
    if len(artifacts) == 0:
        print(f"{args['artifacts']} directory have no files ...")
        return
    args['artifacts'] = artifacts
    upload(args=args)
    

if __name__ == "__main__":
    main()
