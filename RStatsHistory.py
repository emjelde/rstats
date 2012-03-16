#!/usr/bin/python

from collections import namedtuple
import gzip
import struct
import sys

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
        Bandwidth = namedtuple('Bandwidth', 'date down up')

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

    @staticmethod
    def get_date(xtime):
        Date = namedtuple('Date', 'year month day')

        return Date(
            ((xtime >> 16) & 0xFF) + 1900,
            ((xtime >>  8) & 0xFF) + 1,
            xtime & 0xFF)

    @staticmethod
    def to_unit(value, unit=None):
        if unit is not None:
            unit = unit.lower()
        if unit == 'k':
            return value / 1024
        if unit == 'm':
            return value / (1024 * 1024)
        if unit == 'g':
            return value / (1024 * 1024 * 1024)
        return value

    def _print_counters(self, counters, unit=None):
        for counter in counters:
            if counter.date != 0:
                date = self.get_date(counter.date)
                print("{0}/{1}/{2} : Upload {3} : Download {4}".format(
                    date.year, date.month, date.day,
                    self.to_unit(counter.up, unit),
                    self.to_unit(counter.down, unit)))

    def print_daily(self, unit=None):
        self._print_counters(self.daily, unit)

    def print_monthly(self, unit=None):
        self._print_counters(self.monthly, unit)

def main():
    import optparse
    from os.path import isfile
    
    usage = "usage: %prog [options] <filename>"
    parser = optparse.OptionParser(usage)

    parser.add_option("-u", "--unit",
                      default = None,
                      help = "Units b (bytes),k (KiB),m (MiB),g (GiB) default is b")

    options, args = parser.parse_args()

    if len(args) == 1 and isfile(args[0]):
        rstats = RStatsHistory(args[0])

        print("Daily:")
        rstats.print_daily(options.unit)
        print("Monthly:")
        rstats.print_monthly(options.unit)
    else:
        print("Incorrect arguments")
        sys.exit(2)

if __name__ == "__main__":
    main()
