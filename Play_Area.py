import tensorflow as tf
from Balloon_Hover_Env import *

if __name__ == "__main__":
    env = BalloonHoverEnv(render_mode = True)
    # Load the trained model
    custom_objects = {'mse': 'mean_squared_error'}
    model = tf.keras.models.load_model("balloon_dqn_model.h5", custom_objects=custom_objects)

    epsilon = 0.0  # No exploration during testing

    import time

    state = env.reset()
    done = False

    while not done:
        env.render()  # Show environment using PyGame
        time.sleep(0.02)  # Slow down for visibility

        # Reshape state for prediction
        state_input = state.reshape(1, -1)
        
        # Predict Q-values and select best action
        q_values = model.predict(state_input, verbose=0)
        action = q_values.argmax()  # Choose best action

        # Take action in the environment
        next_state, reward, done, _ = env.step(action)
        state = next_state
