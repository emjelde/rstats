#!/usr/bin/python

from collections import namedtuple
import gzip
import struct
import sys

Bandwidth = namedtuple('Bandwidth', 'date up down')
Date = namedtuple('Date', 'year month day')

class RStatsHistory(object):
    ID_V0 = 0x30305352
    ID_V1 = 0x31305352

    def __init__(self, rstats_filename):
        self.daily = []
        self.monthly = []
        self.rstats_file = self._decompress(rstats_filename)
        self._load_history()

    def _decompress(self, filename):
        try:
            return gzip.open(filename, 'rb')
        except IOError as e:
            sys.stderr.write("File could not be decompressed\n")

    def _load_history(self):
        max_daily = 62
        max_monthly = 25

        daily = []
        monthly = []

        version, = struct.unpack("I0l", self.rstats_file.read(8))

        if version == RStatsHistory.ID_V0: 
           max_monthly = 12 

        for i in range(max_daily):
            self.daily.append(Bandwidth._make(struct.unpack("I2Q", self.rstats_file.read(24))))

        dailyp, = struct.unpack("i0l", self.rstats_file.read(8))

        for i in range(max_monthly):
            self.monthly.append(Bandwidth._make(struct.unpack("I2Q", self.rstats_file.read(24))))

        monthlyp, = struct.unpack("i0l", self.rstats_file.read(8))

    def _get_date(self, xtime):
        return Date(
            ((xtime >> 16) & 0xFF) + 1900,
            ((xtime >>  8) & 0xFF) + 1,
            xtime & 0xFF)

    def _to_unit(self, value, unit=None):
        if unit is not None:
            unit.lower()
        if unit == 'k':
            return value / 1024
        if unit == 'm':
            return value / (1024 * 1024)
        elif unit == 'g':
            return value / (1024 * 1024 * 1024)
        return value

    def _print_counters(self, counters, unit=None):
        for counter in counters:
            if counter.date != 0:
                date = self._get_date(counter.date)
                print("{0}/{1}/{2} : Upload {3} : Download {4}".format(
                    date.year, date.month, date.day,
                    self._to_unit(counter.up, unit),
                    self._to_unit(counter.down, unit)))

    def print_daily(self, unit=None):
        self._print_counters(self.daily, unit)

    def print_monthly(self, unit=None):
        self._print_counters(self.monthly, unit)

def main():
    import getopt
    from os.path import isfile
    
    try:
        opts, args =  getopt.getopt(sys.argv[1:], "u:", ["unit"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    unit = None
    filename = sys.argv[-1]

    for o, a in opts:
        if o in ("-u", "--unit"):
            unit = a
        else:
            assert False, "unhandled option"

    if len(sys.argv) > 1 and isfile(filename):
        rstats = RStatsHistory(filename)

        print("Daily:")
        rstats.print_daily(unit)
        print("Monthly:")
        rstats.print_monthly(unit)
    else:
        print_usage("Missing File")
        sys.exit(2)

def print_usage(msg=None):
    if msg is not None:
        print(msg)
    print("usage: [-u --unit K,M,G] <filename>")

if __name__ == "__main__":
    main()
