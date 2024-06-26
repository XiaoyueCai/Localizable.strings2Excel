#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from collections import OrderedDict
from Log import Log
import xml.dom.minidom
import re
import xml.etree.cElementTree as ET


class XmlFileUtil:
    'android strings.xml file util'

    @staticmethod
    def writeToFile(keys, values, directory, filename, additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        fo = open(directory + "/" + filename, "wb")

        stringEncoding = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>\n"
        fo.write(stringEncoding)

        for x in range(len(keys)):
            if values[x] is None or values[x] == '':
                Log.error("Key:" + keys[x] +
                          "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x].strip()
            value = re.sub(r'(%\d\$)(@)', r'\1s', values[x])
            value = re.sub(r"&(?!amp;)", "&amp;", value, re.MULTILINE)
            if not value.startswith("\"") and not value.endswith("\""):
                value = re.sub(r"([^\\])(')", r"\1\'", value, re.MULTILINE)
            value = value.replace("...", "…")
            value = re.sub(r'([^\\])(")', r'\1\"', value, re.MULTILINE)
            content = "   <string name=\"" + key + "\">" + value + "</string>\n"
            fo.write(content)

        if additional is not None:
            fo.write(additional)

        fo.write("</resources>")
        fo.close()

    @staticmethod
    def getKeysAndValues(path):
        if path is None:
            Log.error('file path is None')
            return

        dom = xml.dom.minidom.parse(path)
        root = dom.documentElement
        itemlist = root.getElementsByTagName('string')

        keys = []
        values = []
        keyValues = OrderedDict()
        for index in range(len(itemlist)):
            item = itemlist[index]
            translatable = item.getAttribute("translatable")
            key = item.getAttribute("name")
            try:
                value = item.firstChild.data
            except:
                Log.error('file=' + path + ', key=' + key + "has not data")
                continue
            if translatable != "false":
                keys.append(key)
                values.append(value)
                keyValues[key] = value

        return (keys, values, keyValues)

    @staticmethod
    def get_array_dict(path):
        if path is None:
            Log.error('file path is None')
            return

        dom = ET.parse(path)
        root = dom.getroot()
        array = root[0]

        data = []
        for dict_item in array:
            data_item = {}
            for index in range(0, len(list(dict_item)), 2):
                key_item = dict_item[index]
                value_item = dict_item[index + 1]
                value = value_item.text
                if value_item.tag == 'integer':
                    value = int(value)
                elif value_item.tag == 'real':
                    value = int(value)
                data_item[key_item.text] = value
            data.append(data_item)

        return data
