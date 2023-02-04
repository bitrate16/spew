LICENSE = """
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
"""

import os
import time
import shutil
import argparse

import watchdog
import watchdog.events
import watchdog.observers

from datetime import datetime

def spew_log(*args):
	now = datetime.now()
	now = now.strftime("%d.%m.%Y-%H:%M:%S")

	print(f'[{ now }]', *args)

def backup_dir(relative_path: str):
	"""Make a backup of given directory relative to `args.path` with respect to limit"""

	parent, filename = os.path.split(relative_path)

	# Absolute path
	backup_parent = os.path.join(args.backup, parent)

	# Target path is <hex_ts>.<relative_path_filename>
	backup_filename = f'{ round(time.time() * 1000) :016x}.{ filename }'

	# Make copy
	try:
		# Log on version create
		spew_log('(backup)', os.path.join(args.path, relative_path)) # , ' --> ', os.path.join(backup_parent, backup_filename))

		os.makedirs(backup_parent, exist_ok=True)
		shutil.copy(os.path.join(args.path, relative_path), os.path.join(backup_parent, backup_filename))

		if args.versions is not None and args.versions > 0:
			# Remove excessive backup
			versions = [ f for f in os.listdir(backup_parent) if f[17:] == filename ]

			if len(versions) > args.versions:
				for f in sorted(versions)[:len(versions) - args.versions]:

					# Log on version removal
					spew_log('(remove version)', os.path.join(backup_parent, f))

					try:
						os.remove(os.path.join(backup_parent, f))
					except:
						import traceback
						traceback.print_exc()
	except:
		import traceback
		traceback.print_exc()

class MHandler(watchdog.events.FileSystemEventHandler):

	@staticmethod
	def on_any_event(event: watchdog.events.FileSystemEvent):
		if event.is_directory:
			return

		# Not in backup folder & In target folder
		if os.path.commonpath([args.backup]) != os.path.commonpath([args.backup, event.src_path]) and os.path.commonpath([args.path]) == os.path.commonpath([args.path, event.src_path]):
			if event.event_type == 'created':
				# Spew
				spew_log('(created)', event.src_path)

				# Do a backup
				relpath = os.path.relpath(event.src_path, args.path)
				backup_dir(relpath)
			elif event.event_type == 'modified':
				# Spew
				spew_log('(modified)', event.src_path)

				# Do a backup
				relpath = os.path.relpath(event.src_path, args.path)
				backup_dir(relpath)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='httpim')
	parser.add_argument(
		'-p',
		'--path',
		type=str,
		default='.',
		help='Directory path',
	)
	parser.add_argument(
		'-b',
		'--backup',
		type=str,
		default='.',
		help='Backup directory path, creates __spew_backup__ subdir',
	)
	parser.add_argument(
		'-v',
		'--versions',
		type=int,
		help='Max file versions, will delete old',
	)
	parser.add_argument(
		'-c',
		'--clear',
		action='store_true',
		help='Clear backups',
	)
	parser.add_argument(
		'-l',
		'--license',
		action='store_true',
		help='License',
	)

	args = parser.parse_args()

	if args.license:
		print(LICENSE)
		exit(0)

	# Resolve abspath for root & cache
	args.path = os.path.abspath(args.path)
	args.backup = os.path.join(os.path.abspath(args.backup), '__spew_backup__')

	if not os.path.exists(args.path):
		print(f'Path "{ args.path }" does not exist')
		exit(1)

	if args.clear:
		try:
			shutil.rmtree(args.backup, ignore_errors=True)
		except:
			import traceback
			traceback.print_exc()
		exit(0)

	os.makedirs(args.backup, exist_ok=True)

	# Backup initial directory
	for root, subdirs, files in os.walk(args.path, followlinks=False):

		# No backup backup
		if os.path.commonpath([args.backup]) != os.path.commonpath([args.backup, root]):
			for f in files:
				relpath = os.path.relpath(os.path.join(root, f), args.path)
				backup_dir(relpath)

	# Start watcher
	observer = watchdog.observers.Observer()
	handler = MHandler()
	observer.schedule(handler, args.path, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(5)
	except:
		import traceback
		traceback.print_exc()

		observer.stop()

	observer.join()
