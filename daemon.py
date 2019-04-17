import os
import sys
import time
import atexit
import signal


class Daemon(object):
    '''
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    '''

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):

        '''
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        :return:
        '''

        # Do first fork
        self.fork()

        # decouple from parent
        self.dettach_env()

        # do second fork
        self.fork()

        # Flush standard file descriptor
        sys.stdout.flush()
        sys.stderr.flush()

        #
        self.attach_stream('stdin', mode='r')
        self.attach_stream('stdout', mode='a+')
        self.attach_stream('stderr', mode='a+')

        # write pidfile
        self.create_pidfile()

    def attach_stream(self, name, mode):

        '''
        Replaces the stream with new one
        :param name:
        :param mode:
        :return:
        '''

        stream = open(getattr(self, name), mode)
        os.dup2(stream.fileno(), getattr(sys, name).fileno())

    def dettach_env(self):
        os.chdir('/')
        os.setsid()
        os.umask(0)

    def fork(self):

        '''
        Spawn the child process
        :return:
        '''

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

    def create_pidfile(self):
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        '''
        Removes the pidfile on process exit
        :return:
        '''
        os.remove(self.pidfile)

    def start(self):
        '''
        Start the daemon
        :return:
        '''

        # Check for a pidfile to see if the daemon is already running
        pid = self.get_pid()

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def get_pid(self):
        '''
        Returns the PID from pidfile
        :return:
        '''
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except (IOError, TypeError):
            pid = None
        return pid

    def stop(self, silent=False):
        '''
        Stop daemon
        :param silent:
        :return:
        '''
        pid = self.get_pid()

        if not pid:
            if not silent:
                message = 'pidfile %s does not exist. Daemon not running?\n'
                sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write(str(err))
                sys.exit(1)

    def restart(self):
        '''
        Restart daemon
        :return:
        '''
        self.stop(silent=True)
        self.start()

    def run(self):
        return



