#!/usr/bin/env python
import argparse
import sys
import xml.etree.ElementTree as ET

try:
    import shapefile
    shapefile_loaded = True
except ImportError:
    shapefile_loaded = False

from pprint import pprint


class WirelessNetwork(object):
    def __init__(self, essid, lat, lng):
        self.essid = essid
        self.lat = lat
        self.lng = lng


class ShapeFileSerializer(object):
    _serializer_id = 'shapefile'

    def __init__(self, networks):
        if not shapefile_loaded:
            raise Exception('Shapefile serializing requires the pyshp library, which cannot be found.')
        self.networks = networks

    def serialize(self):
        w = shapefile.Writer(shapefile.POINT)
        for network in self.networks:
            w.point(network.lat, network.lng)
        w.save('test')


class KMLSerialzier(object):
    _serializer_id = 'kml'

    def __init__(self, networks):
        self.networks = networks

    def serialize(self):
        raise Exception('KML serializing not implemented yet')


class NetXMLParser(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        root = ET.parse(self.filename).getroot()
        wireless_networks = root.iter('wireless-network')
        return filter(None, [self.parse_network(network) for network in wireless_networks])

    def parse_network(self, network):
        bssid = network.find('BSSID').text
        ssid = network.find('SSID')
        gpsinfo = network.find('gps-info')
        if ssid and gpsinfo:
            essid = ssid.find('essid').text
            lat = float(gpsinfo.find('avg-lat').text)
            lng = float(gpsinfo.find('avg-lon').text)
            return WirelessNetwork(essid, lat, lng)
        return None


def run(input_filename, output_format):
    networks = NetXMLParser(input_filename).parse()
    for c in (KMLSerialzier, ShapeFileSerializer):
        if c._serializer_id == output_format:
            serializer = c(networks)
            serializer.serialize()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kismet GPS Tools')
    parser.add_argument('-i', '--input-file', metavar='input_file', type=str, help='netxml input file', required=True)
    parser.add_argument('-f', '--output-format', metavar='output_format',type=str,
        choices=[c._serializer_id for c in (KMLSerialzier, ShapeFileSerializer)],
        help='output file format', required=True)

    args = parser.parse_args()
    run(args.input_file, args.output_format)
