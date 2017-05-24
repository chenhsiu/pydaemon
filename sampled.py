#!/usr/bin/env python3.5

import daemon.runner
import time
import datetime
import os
import os.path
import sys

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
        self.context = None

    def run(self):
        self.main_loop()

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
    app = App()
    runner = daemon.runner.DaemonRunner(app)
    app.context = runner.daemon_context 
    runner.do_action()

