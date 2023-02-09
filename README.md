# spew
Automatic on change file backuper

# Features
* Lazy
* Backup files on change recursively in specified directory
* Limit amount of versions
* All files are stored in `__spew_backup__` in format `<date_time>.<filename>`
* Good for automatically backing up artworks during many CTRL+S

# Usage
Clone/download & unpack

Use `start` & `clear-cache` scripts to run lazy

```
usage: spew.py [-h] [-p PATH] [-b BACKUP] [-v VERSIONS] [-m MAX_WAIT] [-c] [-l] [-i]

httpim

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Directory path
  -b BACKUP, --backup BACKUP
                        Backup directory path, creates __spew_backup__ subdir
  -v VERSIONS, --versions VERSIONS
                        Max file versions, will delete old versions after making new backup
  -m MAX_WAIT, --max_wait MAX_WAIT
                        Time that should pass since last file change so it would get backed up, in milliseconds (anti-stacking). Represents how often do you press CTRL+S on file. For eample, set to 5000 and file will be saved 5 seconds after last change, that may be useful for very large files
  -c, --clear           Clear backups
  -l, --license         License
  -i, --initial         Make initial backup on start
```

# License
```
spew - Automatic on change directory backuper
Copyright (C) 2023  bitrate16

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
