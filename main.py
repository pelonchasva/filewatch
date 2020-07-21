# Watchdog PyPI: https://pypi.org/project/watchdog/
# http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/
# https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/

import os, sys
from os.path import expanduser
import shutil
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from logger import Logger

HOME = expanduser("~")

log = Logger(__file__)

# File types and folder map
FILE_FOLDER_MAP = {
    "": "Executables",
    "": "Excel",
    "": "PDF",
    "": "Images",
    "": "Videos",
    "": "Music"
}

def get_file_name(path: str):
    """
    """
    filename = None

    try:
        filename = Path(path).name
    except Exception as ex:
        log.error(ex, "An error occurred while retriving the file name.")

    return filename

def create_folder(path: str):
    """
    """
    result = False

    try:
        os.mkdir(path)
        result = True
    except OSError as ex:
        log.error(ex, f"An error occurred while creating the folder in the path '{path}'.")

    return result

class Handler(PatternMatchingEventHandler):
    """
    """
    def __init__(self, dest_path: str, patterns: list, ignore_dir: bool = False, case_sensitive: bool = False):
        PatternMatchingEventHandler.__init__(self, patterns=patterns, ignore_directories=ignore_dir, case_sensitive=case_sensitive)
        self.dest_path = dest_path

    def on_created(self, event):
        log.info(f"{event.src_path} has been created.")
        filename = get_file_name(event.src_path)

        if not os.path.exists(self.dest_path):
            result = create_folder(self.dest_path)

            if not result:
                return
        
        try:
            shutil.move(event.src_path, os.path.join(self.dest_path, filename))
        except Exception as ex:
            log.error(ex, "An error occurred while moving the file.")

    def on_deleted(self, event):
        log.warn(f"{event.src_path} has been deleted.")

    def on_modified(self, event):
        log.warn(f"{event.src_path} has been modified.")

    def on_moved(self, event):
        log.info(f"Moved a file from {event.src_path} to {event.dest_path}")

def main():
    """
    """
    src_path = os.path.join(HOME, "Downloads")
    dest_path = os.path.join(src_path, "Text")

    event_handler = Handler(dest_path=dest_path, patterns=['*.txt', '*.rtf'])
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except Exception as ex:
        log.error(ex, "An error occurred while observing file changes.")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()
