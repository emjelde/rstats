RStats History
=============

Read rstats backup bandwidth usage file created by Tomato (wireless router firmware).

Why?
----

Tomato provides statistics in the form of an "rstats" file. After reading the source
provided in the Tomato project for creating the rstats file these scripts were created
to help parse and format the bandwidth statistics.

See [forum][t-312300] for discussion.

Usage
-----

```sh
$ python RStatsHistory.py --help
Usage: RStatsHistory.py [options] <filename>
Options:
  -h, --help            show this help message and exit
  -u UNIT, --unit=UNIT  Units b (bytes),k (KiB),m (MiB),g (GiB) default is b
$ python RStatsHistory.py tomato_rstats.gz
```

Or

```sh
$ python RStatsOutput.py --help
Usage: RStatsOutput.py [options] <filename>
Options:
  -h, --help            show this help message and exit
  -i INDENT, --indent=INDENT
                        Indent JSON
  -d DAILY, --daily=DAILY
                        Daily units b (bytes),k (KiB),m (MiB),g (GiB) default
                        is b
  -m MONTHLY, --monthly=MONTHLY
                        Monthly units b (bytes),k (KiB),m (MiB),g (GiB)
                        default is b
$ python RStatsOutput.py -dm -mg -i3 tomato_rstats.gz
```

[t-312300]: http://tomatousb.org/forum/t-312300/anyway-to-view-rstats-bandwidth-file-in-clear-text
