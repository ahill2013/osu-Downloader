#!/usr/bin/env python3

import os.path
import sys

from osu_web_connection import *


def read_sync_file(file_name):
    id_list = []
    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            id_list = f.read().splitlines()
    return id_list


def write_sync_file(id_list, file_name):
    with open(file_name, 'w+') as f:
        for entry in id_list:
            f.write(entry + "\n")


def sync_list_update(sync_list, curr_list):
    download_list = []
    for item in sync_list:
        if item not in curr_list:
            download_list.append(item)
    return download_list


def sync_download(new_list, wdir):
    conn = OsuWebConnection()
    for item in new_list:
        conn.download_sync(item, wdir)
    conn.close()


def main(args):
    if args[0] == "sync":
        if len(args) < 2 or not os.path.isdir(args[1]):
            print("Error: download directory not found")
            exit(1)

        wdir = os.path.abspath(args[1])
        os.chdir(wdir)
        file_name = "sync_list.txt"
        sync_list = read_sync_file(file_name)
        all_subdirs = [name for name in os.listdir('.') if os.path.isdir(name)]

        curr_list = []
        for dirs in all_subdirs:
            entry = dirs.split(' ')[0]
            if entry.isdigit():
                curr_list.append(entry)

        new = []
        if sync_list:
            new = sync_list_update(sync_list, curr_list)
            sync_download(new, wdir)

        curr_list.extend(new)
        write_sync_file(curr_list, file_name)
        if new:
            print("Beatmap list synchronized")
        else:
            print("Beatmap list created")


if __name__ == "__main__":
    main(sys.argv[1:])
