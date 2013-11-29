#!/usr/bin/env python
import argparse
import sys

from xml.dom.minidom import parseString


class ShapeFileSerializer(object):
    _serializer_id = 'shapefile'


class KMLSerialzier(object):
    _serializer_id = 'kml'

class NetXMLParser(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename) as input_file:
            input_dom = parseString(input_file)
            wireless_networks = input_dom.getElementsByTagName('wireless-network')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kismet GPS Tools')
    parser.add_argument('-i', '--input-file', metavar='input_file', type=str, help='netxml input file', required=True)
    parser.add_argument('-f', '--output-format', metavar='output_format',type=str,
        choices=[c._serializer_id for c in (KMLSerialzier, ShapeFileSerializer)],
        help='output file format', required=True)

    args = parser.parse_args()
    print(args.input_file, args.output_format)
