#!/usr/bin/env python3
import json
import multiprocessing
import re
import sys
import pathlib

from .utils import add_url, cprint, get_latest, is_updated, query_library
from .build import update_library
from .system import (
    check_zipped_dirs,
    clean_dir_name,
    create_directory,
    get_dirs,
    get_new_count,
    move_to_raw,
    remove_directory,
    return_cmd,
    run_cmd,
    write_recent_updates,
    zip_dirs,
)


def make_item(user, args, max_str, url, title, latest):
    return {
        "user": user,
        "args": args,
        "max_str": max_str,
        "url": url,
        "title": title,
        "latest": latest,
        "updated": False,
        "new_count": 0
    }


def bulk_new(user, args):
    items = []
    if args.max_chapter is None:
        max_str = ""
    else:
        max_str = args.max_chapter
    if args.min_chapter is None:
        latest = 0.0
    else:
        try:
            latest = float(args.min_chapter)
        except ValueError:
            latest = 0.0
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
        items.append(make_item(user, args, max_str, url, title, latest))
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
        max_str = ""
    else:
        max_str = args.max_chapter
    for item in data:
        items.append(
            make_item(
                user, args, max_str, item["url"], item["title"], item["latest"]
            )
        )
    pool = multiprocessing.Pool()
    results = pool.map_async(download_latest, items)
    results.get()
    updated = []
    with open(user.files["library_file"], "r") as data:
        library = json.load(data)
    cprint("green", "Updating library")
    update_library(user, args)
    for title, data in library.items():
        dest = user.settings["base_dir"] + f"/{title}"
        if is_updated(dest, data):
            new_count = get_new_count(dest, get_latest(data))
            updated.append(
                {
                    "title": title,
                    "new_count": new_count
                }
            )
            cprint("cyan", f"Was updated: {title}")
        else:
            cprint("magenta", f"Not updated: {title}")
    if len(updated) != 0:
        cprint("green", f"Documenting updates in '{user.files['updates_file']}'")
        write_recent_updates(user, updated)
    return 0


def download_latest(item):
    user = item["user"]
    # # args = item[1]
    max_str = item["max_str"]
    url = item["url"]
    title = item["title"]
    latest = item["latest"]
    base_dir = user.settings["base_dir"]
    dest = f"{base_dir}/{title}"
    gdl_config_path = user.files["gdl_file"]
    if max_str == "":
        max_count = 9999
    else:
        try:
            max_count = latest + float(max_str)
        except ValueError:
            max_count = latest + 1
    cmd = [
        "gallery-dl",
        "-f", "/O",
        "--config", gdl_config_path,
        "-d", f"{dest}/gallery-dl",
        "--chapter-filter", f"{latest} < chapter <= {max_count}",
        "-o", "cookies.PHPSESSID=aaaaaaaaaaaaaaaaaaaaaaaaaa",
        "--exec-after", f'mv {{_directory}} "{dest}"/',
        url
    ]
    cprint("green", f"Downloading {title}: {url}")
    run_cmd(cmd)
    storage_path = pathlib.Path(dest + "/gallery-dl")
    if storage_path.is_dir():
        remove_directory(storage_path)
        process_dir(base_dir, dest, user)
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


def process_dir(base_dir, dest, user):
    path = pathlib.Path(dest)
    dirs = []
    cprint("yellow", f"Cleaning: {path}")
    for dir in get_dirs(path):
        result = clean_dir_name(dir)
        if result is not None:
            dirs.append(result)
    cprint("yellow", f"Zipping: {path}")
    zip_dirs(dirs, user.settings["zip_cmd"])
    cprint("yellow", f"Checking zips: {path}")
    check_zipped_dirs(dirs, user.settings["zip_cmd"])
    cprint("yellow", f"Moving raws: {path}")
    move_to_raw(base_dir, path)


def update_urls(item):
    user = item["user"]
    url = item["url"]
    title = item["title"]
    base_dir = user.settings["base_dir"]
    dest = f"{base_dir}/{title}"
    cprint("yellow", f"Associating {url} with {title}")
    add_url(url, dest, user)


