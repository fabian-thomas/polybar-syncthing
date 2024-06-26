#!/usr/bin/env -S python3 -u
import sys
import time
import os
from syncthing import Syncthing, SyncthingError
import xml.etree.ElementTree as ET
from threading import Thread

IDLE_ICON = ''
PAUSE_ICON = ''
SYNC_ICON = ''

def get_progress():
    progress_sum = 0
    syncing_folders = 0
    folders = s.sys.config()['folders']
    for f in folders:
        stats = s.db.status(f['id'])
        if stats['state'] == 'syncing':
            syncing_folders += 1
            progress_sum += stats['inSyncBytes']/(stats['inSyncBytes']+stats['needBytes'])

    if syncing_folders == 0:
        return 100
    else:
        return int(progress_sum / syncing_folders * 100)

class ProgressTask:

    def __init__(self):
        self.running = False

    def terminate(self):
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            progress = get_progress()

            # TODO: this makes no difference since we have no mono font
            print('%s %s' % (SYNC_ICON, str(progress).rjust(3)))
            sys.stdout.flush()

            if progress == 100:
                break

            if self.running:
                time.sleep(1)

        self.running = False

# read api key from syncthing config
tree = ET.parse(os.path.join(os.environ.get('XDG_CONFIG_HOME',
        os.path.join(os.environ["HOME"], ".config")), 'syncthing/config.xml'))
api_key = tree.getroot().find('gui').find('apikey').text

s = Syncthing(api_key)

progress_task = ProgressTask()
progress_thread = None

def stop_progress_thread():
    global progress_thread
    if progress_thread != None:
        if not progress_task.running:
            progress_task.terminate()
        progress_thread.join()
        progress_thread = None

def start_progress_thread():
    global progress_thread
    if progress_thread == None and not progress_task.running:
        progress_thread = Thread(target=progress_task.run)
        progress_thread.start()

start_progress_thread()

# Begin long running event stream. We get woken up when an event happens.
while True:
    try:
        event_stream = s.events(limit=10)
        for event in event_stream:
            if s.stats.folder() == {}:
                stop_progress_thread()
                print('%s 100' % PAUSE_ICON)
                sys.stdout.flush()
            elif event['type'] == 'StateChanged':
                if event['data']['to'] == 'syncing':
                    start_progress_thread()
                else:
                    if event['data']['to'] == 'idle':
                        stop_progress_thread()
                        print('%s 100' % IDLE_ICON)
                    else:
                        print('%s %s' % (SYNC_ICON, str(get_progress()).rjust(3)))
                    sys.stdout.flush()

                    # make quick rescans visible
                    time.sleep(0.1)
    except SyncthingError:
        pass
