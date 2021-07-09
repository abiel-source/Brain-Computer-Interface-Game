import time
import os
import numpy as np
import argparse
import random
import sys


# FUNCTIONS
###########
def get_args(isActionRequired=False, isModelRequired=False, isDifficultyRequired=False):
    parser = argparse.ArgumentParser()
    # action
    if isActionRequired:
        parser.add_argument('-ac', '--action', type=str, help='target motor action', required=True)
    else:
        parser.add_argument('-ac', '--action', type=str, help='target motor action', required=False)
    # model
    if isModelRequired:
        parser.add_argument('-md', '--model', type=str, help='neural network model', required=True)
    else:
        parser.add_argument('-md', '--model', type=str, help='neural network model', required=False)
    # difficulty
    if isDifficultyRequired:
        parser.add_argument('-diff', '--difficulty', type=str, help='difficulty level: easy or hard', default="easy", required=True)
    else:
        parser.add_argument('-diff', '--difficulty', type=str, help='difficulty level: easy or hard', default="easy", required=False)
    parser.add_argument('-fps', '--fps', type=int, help='frames per second', required=False, default=30) # sensitive argument, don't change
    parser.add_argument('-freq', '--max_frequency', type=int, help='maximum frequency', required=False, default=120) # sensitive argument, don't change
    parser.add_argument('-dur', '--duration', type=int, help='session duration in seconds', required=False, default=10) # sensitive argument, don't change
    args = parser.parse_args()
    return args

# get_args() example use case:
# 
# ARGS = utils.get_args()
# # MAX_FREQ = ARGS.max_frequency 
# FPS = ARGS.fps
# SESSION_DURATION = ARGS.duration
# TOTAL_SNAPSHOTS = SESSION_DURATION * FPS  # ~30 iters/sec
# ACTION = utils.process_action_input(ARGS.action)

# MODEL_NAME = ARGS.model
# MODEL = tf.keras.models.load_model(MODEL_NAME)
# MODEL.predict(np.zeros((32,8,120)).reshape(RESHAPE))


def process_action_input(action):
    if action not in ['down', 'up', 'randomize']:
        sys.exit("ERROR::INVALID ACTION ARGUMENT")
    
    if action == 'randomize':
        return random.choice(['down', 'up'])
    return action

def process_difficulty_input(difficulty):
    if difficulty not in ['easy', 'hard']:
        sys.exit("ERROR::INVALID DIFFICULTY ARGUMENT")
    return difficulty

def save_session(ACTION, session):
    actiondir = f'data/{ACTION}'
    res = input('\ndo you want to save this session? (y/n) ==> ')
    if res == 'y' or res == 'Y':
        print(f"\nsaving {ACTION} data...")
        session_name = f'{int(time.time())}.npy'
        np.save(os.path.join(actiondir, session_name), np.array(session))
        print(f'session successfully saved as {session_name}.')
    else:
        print('\nsession not saved.')

def summary(ACTION):
    print("\n----------------SUMMARY----------------")
    print(f'TARGET ACTION: {ACTION}\n')
    # number of sessions files
    for action in ['down', 'up']:
        DIR = f'./data/{action}'
        print(f'{action} {len([session for session in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, session))])} session files')
    print()