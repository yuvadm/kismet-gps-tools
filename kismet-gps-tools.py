#!/usr/bin/env python
import argparse
import logging
import sys
import xml.etree.ElementTree as ET

try:
    import shapefile
    shapefile_loaded = True
except ImportError:
    shapefile_loaded = False


class WirelessNetwork(object):
    def __init__(self, essid, lat, lng):
        self.essid = essid
        self.lat = lat
        self.lng = lng


class ShapefileSerializer(object):
    _serializer_id = 'shapefile'

    def __init__(self, networks):
        if not shapefile_loaded:
            raise Exception('Shapefile serializing requires the pyshp library, which cannot be found.')
        self.networks = networks

    def serialize(self):
        logging.info('Applying Shapefile Serializer')
        w = shapefile.Writer(shapefile.POINT)
        for network in self.networks:
            logging.debug('Adding point: {},{}'.format(network.lat, network.lng))
            w.point(network.lng, network.lat)
        w.field('ESSID')
        for network in self.networks:
            logging.debug('Adding ESSID: {}'.format(network.essid))
            w.record(network.essid)
        w.save('shapefiles/networks')
        logging.info('Saved shapefiles to shapefiles/networks.*')


class KMLSerializer(object):
    _serializer_id = 'kml'

    def __init__(self, networks):
        self.networks = networks

    def serialize(self):
        raise Exception('KML serializing not implemented yet')


class CSVSerializer(object):
    _serializer_id = 'csv'

    def __init__(self, networks):
        self.networks = networks

    def serialize(self):
        logging.info('Applying CSV Serializer')
        with open('networks.csv', 'w') as out:
            for network in self.networks:
                logging.debug('Adding point:{},{},{}'.format(network.essid, network.lat, network.lng))
                out.write('{},{},{}\n'.format(network.essid, network.lng, network.lat))
        logging.info('Saved shapefiles to networks.csv')


class NetXMLParser(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        logging.info('Parsing input file {}'.format(self.filename))
        root = ET.parse(self.filename).getroot()
        wireless_networks = root.iter('wireless-network')
        networks = [self.parse_network(network) for network in wireless_networks]
        return [n for n in networks if n]

    def parse_network(self, network):
        bssid = network.find('BSSID').text
        ssid = network.find('SSID')
        gpsinfo = network.find('gps-info')
        if ssid is not None and gpsinfo is not None:
            essid = ssid.find('essid').text
            lat = float(gpsinfo.find('avg-lat').text)
            lng = float(gpsinfo.find('avg-lon').text)
            return WirelessNetwork(essid, lat, lng)
        else:
            logging.debug('Skipping network due to partial data')
            return None


def run(input_filename, output_format, serialize):
    networks = NetXMLParser(input_filename).parse()
    if serialize:
        for c in (KMLSerializer, ShapefileSerializer, CSVSerializer):
            if c._serializer_id == output_format:
                serializer = c(networks)
                serializer.serialize()
    else:
        logging.info('Skipping serialization')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kismet GPS Tools')
    parser.add_argument('-i', '--input-file', metavar='input_file', type=str, help='netxml input file', required=True)
    parser.add_argument('-f', '--output-format', metavar='output_format',type=str,
        choices=[c._serializer_id for c in (KMLSerializer, ShapefileSerializer, CSVSerializer)],
        help='output file format', required=True)
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true', default=False)
    parser.add_argument('-vv', '--veryverbose', help='very verbose output', action='store_true', default=False)
    parser.add_argument('-n', '--noserialize', help='do not create any output', action='store_false', default=True)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.veryverbose:
        logging.basicConfig(level=logging.DEBUG)

    run(args.input_file, args.output_format, serialize=args.noserialize)
