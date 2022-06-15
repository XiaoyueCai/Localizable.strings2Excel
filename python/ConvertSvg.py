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
                      help="svg files directory.",
                      metavar="fileDir")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options


def convert_svg_filename(file_dir):
    for root, _, filenames in os.walk(file_dir):
        svg_filenames = [fi for fi in filenames if fi.endswith(".svg")]
        for svg_filename in svg_filenames:
            svg_path = os.path.join(root, svg_filename)
            after_name = os.path.basename(root).replace(".imageset", ".svg")
            after_svg_path = os.path.join(root, after_name)
            os.rename(svg_path, after_svg_path)

    print "Convert %s successfully!" % file_dir


def start_convert(options):
    file_dir = options.fileDir

    print "Start converting"

    if file_dir is None:
        print "svg files directory can not be empty! try -h for help."
        return

    convert_svg_filename(file_dir)


def main():
    options = add_parser()
    start_convert(options)


main()
