#!/usr/bin/env python3
# bitscalcpro/main.py

import sys
import time
import pkg_resources
from bitscalcpro.welcome import Welcome
from bitscalcpro.validator import Validator
from bitscalcpro.print_info import PrintInfo

class Main:
    """
    Main class for the bitscalcpro application.

    Methods:
    - main(): Main method to execute the application.
    - main_loop(): Main loop for the interactive part of the application, prompting user input and displaying results.
    - handle_cla(): Handles command line arguments, including version check.
    """

    @staticmethod
    def main():
        """
        Entry point for the bitscalcpro application.
        Initiates the application based on command line arguments or starts the main loop for interactive use.
        """
        if len(sys.argv) > 1:
            if sys.argv[1] not in ('--version', '-v'):
                Welcome.wc()
                time.sleep(2)
            Main.handle_cla()
            Main.main_loop()
        else:
            Welcome.wc()
            Main.main_loop()

    @staticmethod
    def main_loop():
        """
        Main loop for the interactive part of the bitscalcpro application.
        Prompts the user to enter a value (float, decimal, hex, octal, or binary),
        validates the input, and prints information about the bits as well as the result.
        """
        while True:
            user_input = input("\033[93mEnter a value (float, decimal, hex, octal, or binary) or press Enter to terminate the program: \033[0m")
            user_input = Validator.input_validation(user_input)
            if user_input is not None:
                PrintInfo.print_bits_info(user_input)
                PrintInfo.print_result(user_input)
            if not user_input:
                print("\033[1;34mProgram terminated.\033[0m")
                break

    @staticmethod
    def handle_cla():
        """
        Handles command line arguments, including version check.
        If the version flag is provided, prints the package version; otherwise, processes the command line argument.
        """
        if sys.argv[1] in ('--version', '-v'):
            try:
                distribution = pkg_resources.get_distribution("bitscalcpro")
                print(f"\033[1;32m{distribution.project_name}\033[0m \033[1;36m{distribution.version}\033[0m")
            except pkg_resources.DistributionNotFound:
                print("Package version not available.")
            sys.exit(0)
        else:
            user_input = Validator.input_validation(sys.argv[1])
            PrintInfo.print_bits_info(user_input)
            PrintInfo.print_result(user_input)

if __name__ == "__main__":
    Main.main()