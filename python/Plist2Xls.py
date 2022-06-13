# -*- coding:utf-8 -*-
import os
import time
from optparse import OptionParser

import pyExcelerator

from Log import Log
from XmlFileUtil import XmlFileUtil


def add_parser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="plist files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the xls files will be saved.",
                      metavar="targetDir")

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
    file_path = os.path.join(dest_dir, "data.xls")
    workbook = pyExcelerator.Workbook()
    ws = workbook.add_sheet(file_path)
    index = 0
    for item in data:
        x = 0
        for key, value in item.items():
            if index == 0:
                ws.write(index, x, key)
            ws.write(index + 1, x, value)
            x += 1
        index += 1
    workbook.save(file_path)
    print "Convert %s successfully! you can see json file in %s" % (
        file_dir, dest_dir)


def gen_dest_dir(target_dir):
    dest_dir = os.path.join(target_dir, "plist-files-to-xls_" + time.strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    return dest_dir


def start_convert(options):
    file_dir = options.fileDir
    target_dir = options.targetDir

    print "Start converting"

    if file_dir is None:
        print "plist files directory can not be empty! try -h for help."
        return

    if target_dir is None:
        print "Target file path can not be empty! try -h for help."
        return

    convert_to_single_file(file_dir, target_dir)


def main():
    options = add_parser()
    start_convert(options)


main()
