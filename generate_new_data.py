import engine
import utils


ARGS = utils.get_args(isActionRequired=True, isModelRequired=True)
ACTION = utils.process_action_input(ARGS.action)
MODEL_NAME = ARGS.model
SESSION_DURATION = ARGS.duration
FPS = ARGS.fps
TOTAL_SNAPSHOTS = SESSION_DURATION * FPS  # ~30 iters/sec
MAX_FREQ = ARGS.max_frequency 

session = engine.run_new_data_loop(ACTION, MODEL_NAME, TOTAL_SNAPSHOTS, FPS, MAX_FREQ)

# keep engine work and utility functions separate
utils.save_session(ACTION, session)
utils.summary(ACTION)

