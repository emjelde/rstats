#!/usr/bin/python

# Copyright (C) 2014 - Evan Mjelde
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
import optparse
from os.path import isfile
from RStatsHistory import RStatsHistory
    
class RStatsOutput(object):
    def __init__(self, rstats):
        self.rstats = rstats

    def to_json(self, unit_daily=None, unit_monthly=None, indent=None):
        day_fmt = []
        month_fmt = []

        for day in self.rstats.daily:
            if day.date != 0:
                day_fmt.append(self.counter(day, unit_daily))
        
        for month in self.rstats.monthly:
            if month.date != 0:
                month_fmt.append(self.counter(month, unit_monthly))
        
        print(json.dumps({
            "daily" : day_fmt,
            "monthly" : month_fmt
        }, sort_keys=True, indent=indent))

    def counter(self, bandwidth, unit):
        return {
            "date" : self.format_date(bandwidth.date),
            "upload" : RStatsHistory.to_unit(bandwidth.up, unit),
            "download" : RStatsHistory.to_unit(bandwidth.down, unit)
        }

    def format_date(self, xtime):
        date = RStatsHistory.get_date(xtime)
        return date.strftime("%Y/%m/%d")

def main():
    usage = "usage: %prog [options] <filename>"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--indent",
                      type=int,
                      default = None,
                      help = "Indent JSON")

    parser.add_option("-d", "--daily",
                      default = None,
                      help = "Daily units b (bytes),k (KiB),m (MiB),g (GiB) default is b")

    parser.add_option("-m", "--monthly",
                      default = None,
                      help = "Monthly units b (bytes),k (KiB),m (MiB),g (GiB) default is b")

    options, args = parser.parse_args()

    if len(args) == 1 and isfile(args[0]):
        history = RStatsHistory(args[0])
        output = RStatsOutput(history)
        output.to_json(options.daily, options.monthly, options.indent)
    else:
        print("Incorrect arguments")
        sys.exit(2)

if __name__ == "__main__":
    main()
