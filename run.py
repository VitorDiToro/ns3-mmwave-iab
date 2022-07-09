#!/usr/bin/python
import os
import re
import sys
import argparse
from datetime import datetime


def get_parameters():
    # Create the parser
    parser = argparse.ArgumentParser(prog='Micro-wave NS3 simulation runner',
                                     description='List arguments options',
                                     fromfile_prefix_chars='@')

    # Add the arguments
    parser.add_argument('-r',
                        metavar='Relays',
                        type=int,
                        action='store',
                        required=True,
                        help='Number of relays to use in simulation')

    parser.add_argument('-t',
                        metavar='Simulation Times',
                        type=int,
                        action='store',
                        required=True,
                        help='Number of time to run the same simulation')

    args = parser.parse_args()
    current_dir_path = sys.argv[0].replace(sys.argv[0].split("/")[-1], '')

    return [args.r, args.t, current_dir_path]


def create_path(current_dir: str, n_relays: int):

    path = f"{current_dir}results/{n_relays}-"
    if n_relays == 1:
        path += "relay/"
    else:
        path += "relays/"
    path += datetime.now().strftime("%Y.%m.%d-%H.%M.%S")

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def execute_simulation():
    os.system("python2 waf configure --build-profile=debug --enable-examples")
    os.system("python2 waf")
    os.system("python2 waf --run mmwave-iab-grid")


def move_results(base_path: str, execution_time: int):
    files_list = ["DataRadioBearerCreatedTrace.txt",
                  "EN-UE.txt",
                  "RlcAmBufferSize.txt",
                  "RxPacketTrace.txt",
                  "StateTransitionTrace.txt",
                  "UdpServerRx.txt",
                  "buildings.txt",
                  "enbs.txt",
                  "ues.txt"]

    folder_path = f"{base_path}/execution-{execution_time}/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for file in files_list:
        print(f"Moved {file}, To {folder_path}")
        os.system(f"mv {file} {folder_path}")


def update_n_relays_in_source_code(current_dir:str, n_relays: int):
    file_name = "mmwave-iab-grid.cc"
    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        new_content = re.sub(r'(numRelays)\s*=\s*\d',
                             r'\1 = {n}'.format(n=n_relays),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()


if __name__ == '__main__':
    n_relays, n_executions, current_dir = get_parameters()
    output_base_path = create_path(current_dir, n_relays)
    update_n_relays_in_source_code(current_dir, n_relays)

    for execution in range(1, n_executions+1):
        execute_simulation()
        move_results(output_base_path, execution)
