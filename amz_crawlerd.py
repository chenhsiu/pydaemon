#!/usr/bin/env python3.5

import daemon
from daemon.runner import make_pidlockfile
import time
import datetime
import os
import os.path
import sys
import signal

class App():
    def __init__(self):
        self.cwd = os.getcwd()
        self.app_name = os.path.basename(__file__).replace('.py', '')
        self.log_dir = '%s/%s' % (self.cwd, 'log')
        self.run_dir = '%s/%s' % (self.cwd, 'run')
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.exists(self.run_dir):
            os.mkdir(self.run_dir)
        self.stdin_path = '/dev/null'
        self.stdout_path = '%s/%s.out' % (self.log_dir, self.app_name)
        self.stderr_path = '%s/%s.err' % (self.log_dir, self.app_name)
        self.pidfile_path = '%s/%s.pid' % (self.run_dir, self.app_name)
        self.pidfile_timeout = 5

    def create(self):
        self.pidfile = make_pidlockfile(self.pidfile_path, self.pidfile_timeout)
        self.context = daemon.DaemonContext(working_directory = self.cwd, 
            stdout = open(self.stdout_path, 'at+', buffering = 1),
            stderr = open(self.stderr_path, 'at+', buffering = 1))
        self.context.pidfile = self.pidfile

    def run(self):
        with self.context:
            self.main_loop()

    def is_running(self):
        if os.path.exists(self.pidfile_path):
            return True
        return False

    def stop(self):
        with open(self.pidfile_path, 'r') as f:
            os.system('kill %s' % f.read())

    def main_loop(self):
        cnt = 0
        while True:
            print('running %d' % cnt)
            cnt += 1
            time.sleep(3)
            if self.context.grace_shutdown:
                print('graceful shutdown')
                break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('%s start|stop|restart' % sys.argv[0])
    else:
        app = App()
        if sys.argv[1] == 'start':
            if app.is_running():
                print('daemon is already running')
            else:
                print('*** start the daemon')
                app.create()
                app.run()
        elif sys.argv[1] == 'stop':
            if app.is_running():
                print('*** stop the daemon')
                app.stop()
            else:
                print('daemon is not running')
        elif sys.argv[1] == 'restart':
            if app.is_running():
                print('*** stop the daemon')
                app.stop()
            print('*** start the daemon')
            app.create()
            app.run()
        else:
            print('wrong command `%s\'' % sys.argv[1])

