
import sys
import os
import argparse
import globals
import json


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version',
                    action='version',
                    version='1.1.4',
                    help="checking version information"
                    )
parser.add_argument('-f', '--config-file',
                    required=True,
                    type=str,
                    help="specifies the configuration file to run")
parser.add_argument('-d', '--disable-config-file-system',
                    required=False,
                    action='store_true',
                    help="disables system setup from configuration file")
parser.add_argument('-l', '--system-node-lib-path',
                    required=False,
                    type=str,
                    help='set custom node library path')
parser.add_argument('-w', '--system-work-dir',
                    required=False,
                    type=str,
                    help='set working directory')
parser.add_argument('--system-aop-log-file',
                    required=False,
                    type=str,
                    help='set aop log file')
parser.add_argument('--system-aop-log-close',
                    required=False,
                    action='store_true',
                    help='set aop log close or not')
parser.add_argument('--system-log-common-log-file',
                    required=False,
                    type=str,
                    help='set common log file')
parser.add_argument('--system-log-function-log-file',
                    required=False,
                    type=str,
                    help='set function log file')


def main():
    args = parser.parse_args()
    if args.config_file is not None:
        config_path = args.config_file
        if not os.path.exists(config_path):
            print("Invalid parameter: {}".format(config_path))
            return
        config = None
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        config['system'] = {'global':{}, 'node_center': {}, 'aop': {}, 'log': {}}
        if args.disable_config_file_system:
            config.pop('system', None)
        if args.system_work_dir is not None:
            config['system']['global']['ENV_WORK_DIR'] = args.system_work_dir
        if args.system_node_lib_path is not None:
            config['system']['node_center']['USER_LIB_PATH'] = args.system_node_lib_path
        if args.system_aop_log_file is not None:
            config['system']['aop']['AOP_LOG_FILE'] = args.system_aop_log_file
        if args.system_aop_log_close:
            config['system']['aop']['LOG_OPEN'] = False
        else:
            config['system']['aop']['LOG_OPEN'] = True
        if args.system_log_common_log_file is not None:
            config['system']['log']['COMMON_LOG_FILE'] = args.system_log_common_log_file
        if args.system_log_function_log_file is not None:
            config['system']['log']['LOG_FILE'] = args.system_log_function_log_file
        globals.init(**config)
        globals.start()
    else:
        parser.print_help()


def run(config):
    with open(config, "r", encoding="utf-8") as f:
        config = json.load(f)
        globals.init(**config)
        globals.start()


if __name__ == '__main__':
    main()
