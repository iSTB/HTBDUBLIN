from liblo import *


class EGGListener(ServerThread):
    def __init__(self, port=9072):
        self.signal = {}
        self.signal['eeg'] = []
        self.signal['alpha_rel'] = []
        self.signal['conc'] = []
        self.signal['mel'] = []
        ServerThread.__init__(self, port)

    # receive accelrometer data
    @make_method('/egg/FZ', 'f')
    def acc_callback(self, path, args):
        print arg
        acc_x, acc_y, acc_z = args
        # print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

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
