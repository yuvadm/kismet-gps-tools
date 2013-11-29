#!/usr/bin/env python2
import argparse
import sys
import xml.etree.ElementTree as ET

from pprint import pprint


class ShapeFileSerializer(object):
    _serializer_id = 'shapefile'


class KMLSerialzier(object):
    _serializer_id = 'kml'


class NetXMLParser(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        root = ET.parse(self.filename).getroot()
        wireless_networks = root.iter('wireless-network')
        for network in wireless_networks:
            self.parse_network(network)

    def parse_network(self, network):
        bssid = network.find('BSSID').text
            ssid = network.find('SSID')
            if ssid:
                print ssid.find('essid').text


def run(input_filename, output_format):
    NetXMLParser(input_filename).parse()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kismet GPS Tools')
    parser.add_argument('-i', '--input-file', metavar='input_file', type=str, help='netxml input file', required=True)
    parser.add_argument('-f', '--output-format', metavar='output_format',type=str,
        choices=[c._serializer_id for c in (KMLSerialzier, ShapeFileSerializer)],
        help='output file format', required=True)

    args = parser.parse_args()
    run(args.input_file, args.output_format)
