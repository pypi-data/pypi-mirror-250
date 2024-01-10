#!/usr/bin/env python3
import multiprocessing
import re
import shlex
import sys
import pathlib

from .utils import add_url, cprint, query_library
from .build import update_library
from .system import (
    check_zips,
    clean_dir_name,
    create_directory,
    get_dirs,
    move_to_raw,
    remove_directory,
    return_cmd,
    run_cmd,
    zip_dirs_in_path,
)


def bulk_new(user, args):
    items = []
    if args.max_chapter is None:
        max = ""
    else:
        max = args.max_chapter
    if args.min_chapter is None:
        start = 0.0
    else:
        try:
            start = float(args.min_chapter)
        except ValueError:
            start = 0.0
    for url in args.add:
        title = get_title(url)
        if title is None:
            cprint(
                "red",
                f"Could not get title, skipping url: {url}",
                out_file=sys.stderr,
            )
            continue
        if not create_directory(
            base_dir=user.settings["base_dir"],
            dir=title,
        ):
            cprint(
                "red",
                f"Could not create directory '{title}' for url: {url}",
                out_file=sys.stderr,
            )
            continue
        items.append((user, args, max, (url, title, start)))
    pool = multiprocessing.Pool()
    results = pool.map_async(download_latest, items)
    results.get()
    cprint("green", "Updating library")
    update_library(user, args)
    for item in items:
        update_urls(item)
    return 0


def bulk_latest(user, args):
    data = query_library(user.files["library_file"])
    items = []
    if args.max_chapter is None:
        max = ""
    else:
        max = args.max_chapter
    for item in data:
        items.append((user, args, max, item))
    pool = multiprocessing.Pool()
    results = pool.map_async(download_latest, items)
    results.get()
    cprint("green", "Updating library")
    update_library(user, args)
    return 0


def download_latest(item):
    user = item[0]
    args = item[1]
    max_str = item[2]
    url = item[3][0]
    title = item[3][1]
    latest = item[3][2]
    base_dir = user.settings["base_dir"]
    dest = f"{base_dir}/{title}"
    gdl_config_path = user.files["gdl_file"]
    if max_str == "":
        max = 9999
    else:
        try:
            max = latest + float(max_str)
        except ValueError:
            max = latest + 1
    cmd = [
        "gallery-dl",
        "-f", "/O",
        "--config", gdl_config_path,
        "-d", f"{dest}/gallery-dl",
        "--chapter-filter", f"{latest} < chapter <= {max}",
        "-o", "cookies.PHPSESSID=aaaaaaaaaaaaaaaaaaaaaaaaaa",
        "--exec-after", f'mv {{_directory}} "{dest}"/',
        url
    ]
    # cmd = shlex.split(
    #     f"""
    #     gallery-dl
    #     -f '/O'
    #     --config "{gdl_config_path}"
    #     -d "{dest}/gallery-dl"
    #     --chapter-filter "{latest} < chapter <= {max}"
    #     -o cookies.PHPSESSID=aaaaaaaaaaaaaaaaaaaaaaaaaa
    #     --exec-after 'mv {{_directory}} "{dest}"/'
    #     "{url}"
    #     """
    # )
    cprint("green", f"Downloading {title}: {url}")
    run_cmd(cmd)
    storage_path = pathlib.Path(dest + "/gallery-dl")
    if storage_path.is_dir():
        remove_directory(storage_path)
        process_dir(base_dir=base_dir, dir=dest, user=user)
    cprint("green", f"Finished {title}: {url}")


def get_title(url):
    result = return_cmd(["gallery-dl", "-K", url])

    if result["stderr"] != "":
        return None
    pattern = r"manga\n\s+(.+)\n"
    match = re.search(pattern, result["stdout"])
    if match:
        return match.group(1)
    else:
        return None


def process_dir(base_dir, dir, user):
    path = pathlib.Path(base_dir, dir)
    subdirs = get_dirs(path)
    cprint("yellow", f"Cleaning: {path}")
    for subdir in subdirs:
        clean_dir_name(subdir)
    cprint("yellow", f"Zipping: {path}")
    zip_dirs_in_path(path, user.settings["zip_cmd"])
    cprint("yellow", f"Checking zips: {path}")
    check_zips(path, user.settings["zip_cmd"])
    cprint("yellow", f"Moving raws: {path}")
    move_to_raw(base_dir, path)


def update_urls(item):
    user = item[0]
    url = item[3][0]
    title = item[3][1]
    base_dir = user.settings["base_dir"]
    dest = f"{base_dir}/{title}"
    cprint("yellow", f"Associating {url} with {title}")
    add_url(url, dest, user)


