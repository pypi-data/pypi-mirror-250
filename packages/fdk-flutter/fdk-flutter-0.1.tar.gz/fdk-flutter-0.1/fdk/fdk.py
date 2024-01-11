import argparse
from mycolorlogger.mylogger import log
from core.utility import is_valid_project_name
import sys

def main():
    parser = argparse.ArgumentParser(description="this tool will help you to create default mvvm pattern for your flutter project")
    parser.add_argument("--startproject", help="create the new flutter project")
    args = parser.parse_args()
    if args.startproject:
        flag = is_valid_project_name(args.startproject)
        if flag:
            log.logger.info("Creating project: " + args.startproject)
        else:
            log.logger.critical("make sure project name contain only a-z and _(underscore)")
            sys.exit()
        # Add your code to explain the URL here
    else:
        log.logger.critical("Error: Please provide the required argument")

if __name__ == "__main__":
    main()