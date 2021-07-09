import engine
import utils


ARGS = utils.get_args(isActionRequired=True)
ACTION = utils.process_action_input(ARGS.action)
SESSION_DURATION = ARGS.duration
FPS = ARGS.fps
TOTAL_SNAPSHOTS = SESSION_DURATION * FPS  # ~30 iters/sec
MAX_FREQ = ARGS.max_frequency 


# constructing base_data_loop() in engine.py has noticably faster execution time, as 
# opposed to constructing and executing it in generate_base_data.py.
# 
# for this reason, session data is built in engine.py as well, and not specified here.
#
# note that python imports are run once only. Therefore, we can import our bci values
# to both this file as well as engine.py.
session = engine.run_base_data_loop(ACTION, TOTAL_SNAPSHOTS, FPS, MAX_FREQ)

# keep engine work and utility functions separate
utils.save_session(ACTION, session)
utils.summary(ACTION)