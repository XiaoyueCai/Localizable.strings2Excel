# -*- coding:utf-8 -*-

import os
import re
import time
from optparse import OptionParser

from Log import Log
from XlsFileUtil import XlsFileUtil
from XmlFileUtil import XmlFileUtil

def addParser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="Xlsx files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the xml files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--excelStorageForm",
                      type="string",
                      default="single",
                      help="The excel(.xlsx) file storage forms including single(single file), multiple(multiple files), default is single.",
                      metavar="excelStorageForm")

    parser.add_option("-a", "--additional",
                      help="additional info.",
                      metavar="additional")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options

def convertFromSingleForm(options, fileDir, targetDir):
    for _, _, filenames in os.walk(fileDir):
        xlsFilenames = [fi for fi in filenames if fi.endswith(".xlsx")]
        for file in xlsFilenames:
            xlsFileUtil = XlsFileUtil(os.path.join(fileDir, file))
            table = xlsFileUtil.getTableByIndex(0)
            firstRow = [cell.value for cell in table[1] if cell.value]
            keys = []
            for row in table.iter_rows(min_row=1, max_row=table.max_row, min_col=1, max_col=1):
                if row[0].value:
                    keys.append(row[0].value)
            del keys[0]

            for index in range(len(firstRow)):
                if index <= 0:
                    continue
                languageName = firstRow[index]
                values = []
                for row in table.iter_rows(min_row=1, max_row=table.max_row, min_col=(index + 1), max_col=(index + 1)):
                    values.append(row[0].value)
                del values[0]

                if languageName == "zh-Hans":
                    languageName = "zh-rCN"
                elif languageName == "zh-Hant":
                    languageName = "zh-rTW"
                else:
                    match = re.match(r"^([a-z]{2})-([A-Z]{2})$", languageName)
                    if match:
                        languageName = match.group(1) + "-r" + match.group(2)

                path = os.path.join(targetDir, "values-" + languageName)
                if languageName == 'en':
                    path = os.path.join(targetDir, "values")
                filename = "strings.xml"
                XmlFileUtil.writeToFile(
                    keys, values, path, filename, options.additional)
    print("Convert %s successfully! you can find xml files in %s" % (
        fileDir, targetDir))

def convertFromMultipleForm(options, fileDir, targetDir):
    for _, _, filenames in os.walk(fileDir):
        xlsFilenames = [fi for fi in filenames if fi.endswith(".xlsx")]
        for file in xlsFilenames:
            xlsFileUtil = XlsFileUtil(os.path.join(fileDir, file))

            languageName = file.replace(".xlsx", "")
            if languageName == "zh-Hans":
                languageName = "zh-rCN"
            path = os.path.join(targetDir, "values-" + languageName)
            if languageName == 'en':
                path = os.path.join(targetDir, "values")
            if not os.path.exists(path):
                os.makedirs(path)

            for table in xlsFileUtil.getAllTables():
                # TODO 适配多个表格转换
                keys = table.col_values(0)
                values = table.col_values(1)
                filename = table.name.replace(".strings", ".xml")

                XmlFileUtil.writeToFile(
                    keys, values, path, filename, options.additional)
    print("Convert %s successfully! you can find xml files in %s" % (
        fileDir, targetDir))

def startConvert(options):
    fileDir = options.fileDir
    targetDir = options.targetDir

    print("Start converting")

    if fileDir is None:
        print("xls files directory can not be empty! try -h for help.")
        return

    if targetDir is None:
        print("Target file path can not be empty! try -h for help.")
        return

    targetDir = targetDir + "/xls-files-to-xml_" + \
        time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    if options.excelStorageForm == "single":
        convertFromSingleForm(options, fileDir, targetDir)
    else:
        convertFromMultipleForm(options, fileDir, targetDir)

def main():
    options = addParser()
    startConvert(options)

if __name__ == "__main__":
    main()