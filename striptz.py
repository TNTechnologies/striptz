#!/usr/bin/python
import logging
from scapy.all import *
from daemon import Daemon

PIDFILE = '/var/run/striptz.pid'
LOGFILE = '/var/run/striptz.log'
CONFIGFILE = '/etc/striptz/striptz.conf'

# Logging configuration
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)

class Striptz(Daemon):

    def run(self):
        #Define application here
        try:
            sniff(prn=strip_tzsp, filter='port 37008', store=0)

        except Exception as e:
            logging.exception('%s' % e)

def strip_tzsp(pkt):
    decapsulated_pkt = Ether(bytes(pkt.payload.payload.payload)[5:])
    sendp(decapsulated_pkt, iface='eth1' , realtime=True)

if __name__ == '__main__':

    daemon = Striptz(PIDFILE)

    if len(sys.argv) == 2:

        if 'start' == sys.argv[1]:
            print('starting...')
            try:
                daemon.start()
            except:
                pass

        elif 'stop' == sys.argv[1]:
            print('Stopping...')
            daemon.stop()

        elif 'restart' == sys.argv[1]:
            print('Restarting...')
            daemon.restart()

        elif 'status' == sys.argv[1]:
            try:
                pf = open(PIDFILE,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None
            except SystemExit:
                pid = None

            if pid:
                print('Striptz is running as pid %s' %pid)
            else:
                print('Striptz is not running')

        else:
            print('Unknown command')
            sys.exit(2)
            #sys.exit(0)

    else:
        print('Usage: %s start|stop|restart|status' % sys.argv[0])
        sys.exit(2)
