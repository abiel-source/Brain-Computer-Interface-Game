import engine
import utils

ARGS = utils.get_args(isModelRequired=True, isDifficultyRequired=True)
MODEL_NAME = ARGS.model
FPS = ARGS.fps
MAX_FREQ = ARGS.max_frequency 
DIFFICULTY = utils.process_difficulty_input(ARGS.difficulty)

engine.run_main_loop(MODEL_NAME, FPS, MAX_FREQ, DIFFICULTY)