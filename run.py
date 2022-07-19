#!/usr/bin/python
import os
import re
import sys
import argparse
from datetime import datetime
import shutil


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
    
    parser.add_argument('-s',
                        metavar='Seed',
                        type=int,
                        action='store',
                        required=True,
                        default=1,
                        help='Random seed (Default: 1)') 
      
    parser.add_argument('-c',
                        metavar='Schedule: RR/PF',
                        type=str,
                        action='store',
                        required=False,
                        choices=["RF", "rf", "PF", "pf"],
                        default="RR",
                        help='Type of schedule used on simulation. RR(Round Robin) or PF(Proportional Fair)')
                            
    parser.add_argument('-n',
                        metavar='Execution number',
                        type=int,
                        action='store',
                        required=True,
                        default=0,
                        help='Define execution RUN on RngSeedManager (Default: 0)') 

    args = parser.parse_args()
    current_dir_path = sys.argv[0].replace(sys.argv[0].split("/")[-1], '')
    
    n_relays = args.r
    simulation_times = args.t
    seed = args.s
    schedule = args.c
    run_turn = args.n

    return [n_relays , simulation_times, seed, schedule, run_turn, current_dir_path]


def create_path(current_dir: str, n_relays: int, seed: int, run: int):

    path = f"{current_dir}results/{n_relays}-"
    if n_relays in [0,1]:
        path += "relay/"
    else:
        path += "relays/"
        
    path += f"seed {seed}/"
    path += f"run {run}/"
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
                  "ENB-UE.txt",
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
        shutil.move(file, folder_path)
        # os.system(f"mv {file} {folder_path}")


def update_n_relays_in_source_code(current_dir:str, n_relays: int):
    file_name = "mmwave-iab-grid.cc"
    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        new_content = re.sub(r'(numRelays)\s*=\s*\d+',
                             r'\1 = {n}'.format(n=n_relays),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def update_seed_in_source_code(current_dir:str, seed: int):
    file_name = "mmwave-iab-grid.cc"
    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(RngSeedManager::SetSeed)\s*\(\d+\)',
                             r'\1({n})'.format(n=seed),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def update_run_turn_in_source_code(current_dir:str, run: int):
    file_name = "mmwave-iab-grid.cc"
    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(unsigned run)\s*=\s*\d+',
                             r'\1 = {n}'.format(n=run),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()


if __name__ == '__main__':
    n_relays, n_executions, seed, schedule_type, run_number, current_dir = get_parameters()
    output_base_path = create_path(current_dir, n_relays, seed, run_number)
    update_n_relays_in_source_code(current_dir, n_relays)
    update_seed_in_source_code(current_dir, seed)
    update_run_turn_in_source_code(current_dir, run_number)
    
    for execution in range(1, n_executions+1):
        execute_simulation()
        move_results(output_base_path, execution)
