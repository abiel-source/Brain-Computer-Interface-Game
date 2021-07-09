from pylsl import StreamInlet, resolve_stream

# SAMPLING FREQUENCY OF 8CH ==> 250HZ ==> MAX_REQ = 120 (roughly 250hz / 2)**
# DATA FORMAT ==> FFS (THROUGH LSL)**
# NUM CHANNELS ==> 125 (THROUGH LSL)**


# FUNCTIONS
###########
def get_eeg_connection():
    print("\nlooking for an EEG stream...")
    STREAMS = resolve_stream('type', 'EEG')
    INLET = StreamInlet(STREAMS[0])
    print('\nEEG Stream Connection Established\n')
    return INLET

# article for why we need maximum frequency of 120 here
# https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem
# 
# note that we do not actually invoke this function in engine.py, instead
# we optimize via inline function call, as every millisecond counts during execution.
def capture_snapshot(MAX_FREQ=120):
    snapshot = []
    for i in range(8):
        sample, timestamp = INLET.pull_sample() # use global INLET variable
        snapshot.append(sample[:MAX_FREQ])
    return snapshot


# SETTINGS
##########
ACTIONS = ['none', 'jump']
RESHAPE = (-1, 8, 120)


# ESTABLISH CONNECTION
######################
INLET = get_eeg_connection()