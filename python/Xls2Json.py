# -*- coding:utf-8 -*-
import json
from optparse import OptionParser

from Log import Log
from XlsFileUtil import XlsFileUtil


def add_parser():
    parser = OptionParser()

    parser.add_option("-f", "--target_file",
                      help="Xls files directory.",
                      metavar="target_file")

    parser.add_option("-o", "--output_path",
                      help="The path where the json files will be saved.",
                      metavar="output_path")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options


def convert_from_single_form(target_file, output_path):
    data = []
    xls_file_util = XlsFileUtil(target_file)
    table = xls_file_util.getTableByIndex(0)
    item_keys = table.row_values(0)

    for index in range(1, table.nrows):
        item_values = table.row_values(index)
        item = {}
        for y in range(table.ncols):
            key = item_keys[y]
            value = item_values[y]
            if type(value) == float:
                if value == int(value):
                    value = int(value)
            # if key == 'name':
            #     value = '${%s}' % value
            item[key] = value
        data.append(item)

    with open(output_path, "w") as w:
        w.write(json.dumps(data))

    print "Convert %s successfully! you can json files in %s" % (
        target_file, output_path)


def start_convert(options):
    target_file = options.target_file
    output_path = options.output_path

    print "Start converting"

    if target_file is None:
        print "xls file can not be empty! try -h for help."
        return

    if output_path is None:
        print "Output file path can not be empty! try -h for help."
        return

    convert_from_single_form(target_file, output_path)


def main():
    options = add_parser()
    start_convert(options)


main()
