# -*- coding:utf-8 -*-
import json
import os
from optparse import OptionParser
from XmlFileUtil import XmlFileUtil
from Log import Log
import time


def add_parser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="plist files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the json files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--jsonStorageForm",
                      type="string",
                      default="single",
                      help="The json file storage forms including single(single file), multiple(multiple files), default is single.",
                      metavar="jsonStorageForm")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options


def convert_to_single_file(file_dir, target_dir):
    dest_dir = gen_dest_dir(target_dir)
    data = []
    for _, _, filenames in os.walk(file_dir):
        plist_filenames = [fi for fi in filenames if fi.endswith(".plist")]
        for plist_filename in plist_filenames:
            plist_path = os.path.join(file_dir, plist_filename)
            data.extend(XmlFileUtil.get_array_dict(plist_path))
    file_path = os.path.join(dest_dir, "data.json")
    with open(file_path, "w") as w:
        w.write(json.dumps(data))
    print "Convert %s successfully! you can see json file in %s" % (
        file_dir, dest_dir)


def convert_to_file(file_dir, target_dir):
    dest_dir = gen_dest_dir(target_dir)

    for _, _, filenames in os.walk(file_dir):
        plist_filenames = [fi for fi in filenames if fi.endswith(".plist")]
        for plist_filename in plist_filenames:
            file_name = plist_filename.replace(".plist", ".json")
            plist_path = os.path.join(file_dir, plist_filename)
            file_path = os.path.join(dest_dir, file_name)
            if not os.path.exists(file_path):
                data = XmlFileUtil.get_array_dict(plist_path)
                with open(file_path, "w") as w:
                    w.write(json.dumps(data))
    print "Convert %s successfully! you can see json file in %s" % (
        file_dir, dest_dir)


def gen_dest_dir(target_dir):
    dest_dir = os.path.join(target_dir, "plist-files-to-json_" + time.strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    return dest_dir


def start_convert(options):
    file_dir = options.fileDir
    target_dir = options.targetDir
    storage = options.jsonStorageForm

    print "Start converting"

    if file_dir is None:
        print "plist files directory can not be empty! try -h for help."
        return

    if target_dir is None:
        print "Target file path can not be empty! try -h for help."
        return

    if storage == 'single':
        convert_to_single_file(file_dir, target_dir)
    else:
        convert_to_file(file_dir, target_dir)


def main():
    options = add_parser()
    start_convert(options)


main()
