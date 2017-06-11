from liblo import *
import sys
import os

class MuseServer(ServerThread):
    def __init__(self, port=5000):
        self.signal = {}
        self.signal['eeg'] = []
        self.signal['alpha_rel'] = []
        self.signal['conc'] = []
        self.signal['mel'] = []
        ServerThread.__init__(self, port)

    # receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        # print("%s %f %f %f" % (path, acc_x, acc_y, acc_z))

    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        self.signal['eeg'].append(args)

        # receive alpha relative data
    @make_method('/muse/elements/alpha_relative', 'ffff')
    def alpha_callback(self, path, args):
        self.signal['alpha_rel'].append(args)

    # receive alpha relative data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        self.signal['conc'].append(args[0])


    # receive mellow data - viewer is the same as concentration
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        self.signal['mel'].append(args[0])
    # handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        test = args
        # print("Unknown message \n\t Source: '%s' \n\t Address: '%s' \n\t Types: '%s ' \n\t Payload: '%s'" %
        # (src.url, path, types, args))




#######Starting Server ################
try:
    server = MuseServer()
except ServerError as err:
    print(str(err))
    sys.exit()
server.start()

print("MuseServer started on port 4444")
while True:
   mel_old = server.signal['mel']
   print(mel_old)
