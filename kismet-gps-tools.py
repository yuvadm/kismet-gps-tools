#!/usr/bin/env python
import sys


class ShapeFileSerializer(object):
    pass


class KMLSerialzier(object):
    pass


def usage():
    print('python kismet-gps-tools.py <input>')
    print('\n')
    exit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
