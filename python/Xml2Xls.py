# -*- coding:utf-8 -*-

import os
from optparse import OptionParser
from XmlFileUtil import XmlFileUtil
import pyExcelerator
from Log import Log
import time


def addParser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="strings.xml files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the xls files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--excelStorageForm",
                      type="string",
                      default="single",
                      help="The excel(.xls) file storage forms including single(single file), multiple(multiple files), default is single.",
                      metavar="excelStorageForm")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options


def convertToMultipleFiles(fileDir, targetDir):
    destDir = genDestDir(targetDir)

    for _, dirnames, _ in os.walk(fileDir):
        valuesDirs = [di for di in dirnames if di.startswith("values")]
        for dirname in valuesDirs:
            workbook = pyExcelerator.Workbook()
            for _, _, filenames in os.walk(os.path.join(fileDir, dirname)):
                xmlFiles = [fi for fi in filenames if fi.endswith(".xml")]
                for xmlfile in xmlFiles:
                    ws = workbook.add_sheet(xmlfile)
                    path = os.path.join(fileDir, dirname, xmlfile)
                    (keys, values, _) = XmlFileUtil.getKeysAndValues(path)
                    for keyIndex in range(len(keys)):
                        key = keys[keyIndex]
                        value = values[keyIndex]
                        ws.write(keyIndex, 0, key)
                        ws.write(keyIndex, 1, value)
            filePath = os.path.join(destDir, getCountryCode(dirname) + ".xls")
            workbook.save(filePath)
    print "Convert %s successfully! you can see xls file in %s" % (
        fileDir, destDir)


def convertToSingleFile(file_dir, target_dir):
    dest_dir = genDestDir(target_dir)
    default_key_values = {}

    for _, dir_names, _ in os.walk(file_dir):
        if "values" in dir_names:
            dir_names.remove("values")
            dir_names.insert(0, "values")
        values_dirs = [di for di in dir_names if di.startswith("values")]
        for dir_name in values_dirs:
            for _, _, filenames in os.walk(os.path.join(file_dir, dir_name)):
                xml_file = "strings.xml"
                file_name = xml_file.replace(".xml", "")
                file_path = os.path.join(dest_dir, file_name + ".xls")
                if not os.path.exists(file_path):
                    workbook = pyExcelerator.Workbook()
                    ws = workbook.add_sheet(file_name)
                    index = 0
                    for dir_name in dir_names:
                        path = os.path.join(file_dir, dir_name, xml_file)
                        if os.path.exists(path):
                            if index == 0:
                                ws.write(0, 0, 'keyName')
                            country_code = getCountryCode(dir_name)
                            ws.write(0, index + 1, country_code)
                            (keys, values, keyValues) = XmlFileUtil.getKeysAndValues(path)
                            x = 0
                            if dir_name == "values":
                                default_key_values = keyValues
                            for key, value in default_key_values.items():
                                rel_value = keyValues[key] if key in keyValues else ""
                                if index == 0:
                                    ws.write(x + 1, 0, key)
                                    ws.write(x + 1, 1, rel_value)
                                else:
                                    ws.write(x + 1, index + 1, rel_value)
                                x += 1
                            index += 1
                    workbook.save(file_path)
    print "Convert %s successfully! you can see xls file in %s" % (
        file_dir, dest_dir)


def genDestDir(targetDir):
    destDir = os.path.join(targetDir, "xml-files-to-xls_" + time.strftime("%Y%m%d_%H%M%S"))
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    return destDir


def getCountryCode(dirname):
    code = 'en'
    dirSplit = dirname.split('values-')
    if len(dirSplit) > 1:
        code = dirSplit[1]
    return code


def startConvert(options):
    fileDir = options.fileDir
    targetDir = options.targetDir

    print "Start converting"

    if fileDir is None:
        print "strings.xml files directory can not be empty! try -h for help."
        return

    if targetDir is None:
        print "Target file path can not be empty! try -h for help."
        return

    if options.excelStorageForm == "single":
        convertToSingleFile(fileDir, targetDir)
    else:
        convertToMultipleFiles(fileDir, targetDir)


def main():
    options = addParser()
    startConvert(options)


main()
