#!/usr/bin/python

import os
import re
import sys
import argparse
from datetime import datetime

BIN_RR_FILE_NAME = "mmwave-iab-grid"
BIN_PF_FILE_NAME = "mmwave-iab-grid-PF"
CPP_PF_FILE_NAME = "mmwave-iab-grid-PF.cc"
CPP_RR_FILE_NAME = "mmwave-iab-grid.cc"

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
                        required=False,
                        default=1,
                        help='Number of times to run the same simulation')
    
    parser.add_argument('-s',
                        metavar='Seed',
                        type=int,
                        action='store',
                        required=False,
                        default=1,
                        help='Random seed (Default: 1)') 
      
    parser.add_argument('-c',
                        metavar='Schedule: RR/PF',
                        type=str,
                        action='store',
                        required=True,
                        choices=["RR", "rr", "PF", "pf"],
                        default="RR",
                        help='Type of schedule used on simulation. RR(Round Robin) or PF(Proportional Fair)')
                            
    parser.add_argument('-n',
                        metavar='Execution RUN number',
                        type=int,
                        action='store',
                        required=False,
                        default=0,
                        help='Define execution RUN on RngSeedManager (Default: 0)') 

    parser.add_argument('-u',
                        metavar='Number of UEs',
                        type=int,
                        action='store',
                        required=True,
                        help='Define de number of UEs in simulation') 

    parser.add_argument('-i',
                        metavar='interPacketInterval',
                        type=int,
                        action='store',
                        required=True,
                        help='Define interPacketInterval -  50 us = 224 Mbits | 200 us = 56 Mbits | 400 us = 28 Mbits') 

                        

    args = parser.parse_args()
    current_dir_path = sys.argv[0].replace(sys.argv[0].split("/")[-1], '')
    
    n_relays = args.r
    simulation_times = args.t
    seed = args.s
    schedule = args.c
    run_turn = args.n
    num_ues = args.u
    inter_packet_interval = args.i

    return [n_relays , simulation_times, seed, schedule, run_turn, num_ues, inter_packet_interval, current_dir_path]


def create_path(current_dir: str, n_relays: int, seed: int, run: int, schedule_type: str, num_ues: str, inter_packet_interval: str):

    path = f"{current_dir}results/{schedule_type.upper()}/"

    path += f"{num_ues}UEs/"
    path += f"{inter_packet_interval}us/"
    
    path += f"{n_relays}-"
    if n_relays in [0,1]:
        path += "relay/"
    else:
        path += "relays/"
        
    path += f"seed-{seed}/"
    path += f"run-{run}/"
    path += datetime.now().strftime("%Y.%m.%d-%H.%M.%S")

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def execute_simulation(schedule_type: str):
    os.system("python2 waf configure --build-profile=debug --enable-examples")
    os.system("python2 waf")
    
    if schedule_type.upper() == "RR":
        os.system(f"python2 waf --run {BIN_RR_FILE_NAME}")
    else:
        os.system(f"python2 waf --run {BIN_PF_FILE_NAME}")


def move_results(base_path: str, execution_number: int):
    files_list = ["DataRadioBearerCreatedTrace.txt",
                  "ENB-UE.txt",
                  "RlcAmBufferSize.txt",
                  "RxPacketTrace.txt",
                  "StateTransitionTrace.txt",
                  "UdpServerRx.txt",
                  "buildings.txt",
                  "enbs.txt",
                  "ues.txt"]

    folder_path = f"{base_path}/execution-{execution_number}/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for file in files_list:
        print(f"Moved {file}, To {folder_path}")
        #shutil.move(file, folder_path)
        os.system(f"mv {file} {folder_path}")


def update_n_relays_in_source_code(current_dir:str, n_relays:int, schedule_type:str):
    if schedule_type.upper() == "RR":
        file_name = CPP_RR_FILE_NAME
    else:
        file_name = CPP_PF_FILE_NAME
    
    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        new_content = re.sub(r'(numRelays)\s*=\s*\d+',
                             r'\1 = {n}'.format(n=n_relays),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def update_seed_in_source_code(current_dir:str, seed: int, schedule_type:str):
    if schedule_type.upper() == "RR":
        file_name = CPP_RR_FILE_NAME
    else:
        file_name = CPP_PF_FILE_NAME

    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(RngSeedManager::SetSeed)\s*\(\d+\)',
                             r'\1({n})'.format(n=seed),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def update_run_turn_in_source_code(current_dir:str, run: int, schedule_type:str):
    if schedule_type.upper() == "RR":
        file_name = CPP_RR_FILE_NAME
    else:
        file_name = CPP_PF_FILE_NAME

    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(unsigned run)\s*=\s*\d+',
                             r'\1 = {n}'.format(n=run),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()


def update_number_of_ues_in_source_code(current_dir:str, num_ues: int, schedule_type:str):
    if schedule_type.upper() == "RR":
        file_name = CPP_RR_FILE_NAME
    else:
        file_name = CPP_PF_FILE_NAME

    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(ueNodes.Create)\(\d+\)',
                             r'\1({n})'.format(n=num_ues),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()


def update_inter_packet_interval_in_source_code(current_dir:str, inter_packet_interval: int, schedule_type:str):
    if schedule_type.upper() == "RR":
        file_name = CPP_RR_FILE_NAME
    else:
        file_name = CPP_PF_FILE_NAME

    file_path = f"{current_dir}scratch/{file_name}"
    with open(file_path, 'r+') as file:
        content = file.read()
        
        new_content = re.sub(r'(uint32_t interPacketInterval)\s*=\s*\d+',
                             r'\1 = {n}'.format(n=inter_packet_interval),
                             content, flags=re.M)
        file.seek(0)
        file.write(new_content)
        file.truncate()


if __name__ == '__main__':
    n_relays, n_executions, seed, schedule_type, run_number, num_ues, inter_packet_interval, current_dir = get_parameters()
    output_base_path = create_path(current_dir, n_relays, seed, run_number, schedule_type, num_ues, inter_packet_interval)
    update_n_relays_in_source_code(current_dir, n_relays, schedule_type)
    update_seed_in_source_code(current_dir, seed, schedule_type)
    update_run_turn_in_source_code(current_dir, run_number, schedule_type)
    update_number_of_ues_in_source_code(current_dir, num_ues, schedule_type)
    update_inter_packet_interval_in_source_code(current_dir, inter_packet_interval, schedule_type)
    
    for execution in range(1, n_executions+1):
        execute_simulation(schedule_type)
        move_results(output_base_path, execution)
