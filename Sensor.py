"""
Libaray to read packages from devices built by Thomas Wennekers. Based on
client.c.

author: Frank Loesche <Frank.Loesche@Plymouth.ac.uk>
"""

import socket
import logging
import time
from datetime import datetime
from struct import unpack

class Sensor(object):

    def __init__(self, sensor_ip, sensor_port=301):
        """
        IP address of the sensor. Port is optional and defaults to 301
        """
        self.sensor_ip = sensor_ip
        self.sensor_port = sensor_port
        self.start = time.time()
        self.count = 0
        self.outfile = None
        self.__open_socket()


    def close(self):
        """
        gracefully close open files and sockets.
        """
        if self.outfile is not None:
            if self.outfile.name:
                logging.info("Closing output file %s" % self.outfile.name)
            self.outfile.close()
            self.outfile = None
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            logging.info("Closing socket to %s:%d" % (self.sensor_ip, self.sensor_port))
        tdiff = time.time() - self.start
        logging.info("received {} packets in {}: {} Hz".format(self.count, tdiff,
            self.count // tdiff))



    def __open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.sensor_ip, self.sensor_port))

    def __save(self, line):
        # import pdb; pdb.set_trace()
        self.outfile.write("%s,%s\n" % (
            datetime.now().strftime('%H:%M:%S.%f'), ','.join(map(str, line))))

    def set_filename(self, filename):
        if filename is None:
            return
        self.outfile = open(filename, 'w')

        self.outfile.write("Connecting to %s at port %d\n" % (self.sensor_ip,
            self.sensor_port))
        tnow = datetime.now()
        self.outfile.write("Current system time : %s\n" % tnow.strftime('%s'))
        self.outfile.write("%s\n" % (tnow.strftime("%Y-%m-%dT%H:%M:%S.%f") ))
        self.outfile.write("Storing data to file '%s'\n" % filename)


    def get_measures(self, packet_length=None, as_float=False, buffer_size=4096):
        """
        returns a generator for the measures received from the sensor. It can be
        called with a fixed packet length. If the packet length is not
        specified, it uses the first byte of the packet as packet length. Buffer
        size is the maximum buffer length to be processed.

        The format is assumed to be <uchar><ulong><ushort>*. This means the
        first byte should be an unsigned char with the length of the package,
        the second a unsingned long with the device ticks (probably
        microseconds), followed by as many unsigned shorts as can fit in the
        packet length. For a packet length of 23 this means 9*<ushort>.
        """
        buffer = b''
        data = True
        pos = 0
        plen = packet_length
        while data:
            data = self.sock.recv(buffer_size)
            if packet_length is None and pos == 0:
                plen = data[0]
            pos += len(data)
            buffer += data
            while pos >= plen:
                self.count += 1
                line = buffer[:plen]
                buffer = buffer[plen:]
                pos = pos-plen
                formatstr = ">BL" + "h"*((plen-5) // 2)
                ret = unpack(formatstr, line)
                if self.outfile is not None:
                    self.__save(ret)
                if as_float:
                    ## assuming elements 0 and 1 are unchangeable, 2 and 3 are
                    ## in the range up to 2^10, and all following ones
                    ## are in the range up 2^16
                    yield ret[:2] \
                        + tuple(map((lambda x: (x + 32767) / 65536.0), ret[2:]))
                        #+ tuple(map((lambda x: x / 1024.0), ret[2:4])) \
                        #+ tuple(map((lambda x: x / 65536.0), ret[5:]))
                else:
                    yield ret
        return
