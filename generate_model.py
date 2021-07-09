import numpy as np
import tensorflow as tf
import os
# from bci import ACTIONS, RESHAPE

ACTIONS = ['down', 'up']
RESHAPE = (-1, 8, 120)

# FUNCTIONS
###########
def load_data(data_dir='data'):
    # objective: load all snapshots recorded ever, for each action.
    # resulting shape should yield --> (x, 8, 120) for each action
    # where x is some large number of snapshots divisible by 300 to get number of session files.
    action_datas = {
        'down': [],
        'up': []
    }
    label_vectors = {
    'down': [1, 0],
    'up': [0, 1]
    }
    combined_data = []
    
    # save all snapshots for each session file into corresponding action array
    for action in ACTIONS:
        data_path = os.path.join(data_dir, action)
        for session_file in os.listdir(data_path):
            session_file_data = np.load(os.path.join(data_path, session_file))
            for snapshot in session_file_data: # each session file should yield 300 of (8 by 120) arrays
                action_datas[action].append(snapshot)
        
        np.random.shuffle(action_datas[action]) # shuffle each action data array
    
    # since numbers of snapshots between action data folders may not be equal.
    min_length = min([len(action_datas[action]) for action in ACTIONS])
    for action in ACTIONS:
        action_datas[action] = action_datas[action][:min_length]
        for snapshot in action_datas[action]:
            combined_data.append([snapshot, label_vectors[action]]) # pair each snapshot X with feature Y
    
    np.random.shuffle(combined_data) # shuffle the combined action data arrays
    
    return combined_data


# CREATE DATA
#############
train_data = load_data(data_dir='data')
train_X = []
train_y = []
for snapshot, label in train_data: # always need to separate features & labels
    train_X.append(snapshot)
    train_y.append(label)

test_data = load_data(data_dir='validation_data')
test_X = []
test_y = []
for snapshot, label in test_data:
    test_X.append(snapshot)
    test_y.append(label)

train_X = np.array(train_X).reshape(RESHAPE)
train_y = np.array(train_y)
test_X = np.array(test_X).reshape(RESHAPE)
test_y = np.array(test_y)


# BUILD MODEL
#############
print('building model')
# model = tf.keras.Sequential(
#     [
#         tf.keras.layers.Flatten(input_shape=(train_X.shape[1:])), # shape of one snapshot
#         tf.keras.layers.Dense(64, activation='relu'),
#         tf.keras.layers.Dense(2, activation='softmax')      # output layer has 2 neurons - down(=0) or up(=1)
#     ]
# )

model = tf.keras.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(train_X.shape[1:])), # shape of one snapshot
        tf.keras.layers.Dense(60, activation='relu'),
        tf.keras.layers.Dense(60, activation='relu'),
        tf.keras.layers.Dense(60, activation='relu'),
        tf.keras.layers.Dense(60, activation='relu'),
        tf.keras.layers.Dense(2, activation=tf.nn.sigmoid)      # output layer has 2 neurons - down(=0) or up(=1)
    ]
)

# NEXT NN ARCHITECTURE TO TRY
# model = tf.keras.Sequential(
#     [
#         tf.keras.layers.Flatten(input_shape=(train_X.shape[1:])), # shape of one snapshot
#         tf.keras.layers.Dense(321, activation='relu'),
#         tf.keras.layers.Dense(321, activation='relu'),
#         tf.keras.layers.Dense(2, activation=tf.nn.sigmoid)      # output layer has 2 neurons - down(=0) or up(=1)
#     ]
# )

# compile as binary classification problem
model.compile(
    optimizer='adam',
    loss='binary_crossentropy', 
    metrics=['accuracy']
)
print('done')


# TRAIN/EVALUATE MODEL
for i in range(8):
    print('training/evaluating model...')
    model.fit(train_X, train_y, epochs=(i))

    loss_val, accuracy_val = model.evaluate(
        test_X, test_y, verbose=1)

    print('final loss =', loss_val)
    print('final accuracy =', accuracy_val)

    # save model
    model.save(f'model-epochs{i}')
print('done.')
