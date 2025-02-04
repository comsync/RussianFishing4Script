"""
Activate game window and start crafting things until running out of materials.

Usage: craft.py
"""
import argparse
import logging
from time import sleep

from prettytable import PrettyTable
import pyautogui as pag

import monitor
from windowcontroller import WindowController
from script import ask_for_confirmation

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Cofigure argparser and parse the command line arguments.

    :return dict-like parsed arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
                        prog='craft.py', 
                        description='Activate game window and start making things until running out of materials', 
                        epilog='')
    parser.add_argument('-d', '--discard', action='store_true',
                            help='discard all the crafted items')
    parser.add_argument('-n', '--quantity', type=int, default=-1,
                            help='the number of item to craft, no limit if not specified')
    return parser.parse_args()
    
if __name__ == '__main__':
    args = parse_args()
    limit = args.quantity
    enable_discard = args.discard
    success_count = 0
    fail_count = 0

    ask_for_confirmation('Are you ready to start crafting')
    WindowController().activate_game_window()

    pag.moveTo(monitor.get_make_position())
    try:
        while True:
            logger.info('Crafting')
            pag.click() # click make button

            # recipe not complete
            if monitor.is_operation_failed():
                logger.warning('Out of materials')
                pag.press('space')
                break

            # crafting, wait for result
            sleep(4)
            while True:
                if monitor.is_operation_success():
                    logger.info('Crafting succeed')
                    success_count += 1
                    break
                elif monitor.is_operation_failed():
                    logger.info('Crafting failed')
                    fail_count += 1
                    break
                sleep(0.25)

            # handle result
            key = 'backspace' if enable_discard else 'space'
            pag.press(key)
            if success_count + fail_count == limit:
                break
            sleep(0.25) # wait for animation
    except KeyboardInterrupt:
        pass
    table = PrettyTable(header=False, align='l')
    table.title = 'Running Results'
    table.add_rows(
        [   
            ['Item crafted', success_count],
            ['Number of failures', fail_count],
            ['Materials used', success_count + fail_count]
        ])
    print(table)