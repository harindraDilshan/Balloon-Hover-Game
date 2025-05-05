from Balloon_Hover_Env import *
from DQNAgent import *
if __name__ == "__main__":
    env = BalloonHoverEnv(render_mode=False)

    state_size = 3  # [height_of_balloon_position, velocity, fan_power]
    action_size = 3  # decrease, stay, increase
    agent = DQNAgent(state_size, action_size)
    episodes = 10
    batch_size = 10

    for e in range(episodes):
        state = env.reset()
        total_reward = 0

        for time_t in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode {e+1}/{episodes}, score: {total_reward}, epsilon: {agent.epsilon:.2f}")
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    # ✅ Save the model after all episodes
    agent.model.save("balloon_dqn_model.h5")
    print("Model saved as balloon_dqn_model.h5")