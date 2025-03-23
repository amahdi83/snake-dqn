import pygame
from snake import SnakeGame
from snake_env import SnakeEnv
from train_agent import DQNAgent

def train_dqn(episodes=100):
    env = SnakeEnv(render_mode=True)
    agent = DQNAgent(state_size=7, action_size=3)

    scores = []

    for e in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            total_reward += reward

        scores.append(total_reward)
        print(f"Episode {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2f}")
    
    agent.save()
    return scores



def watch_trained_agent(agent_path="dqn_snake.pth", episodes=1000, delay=50):
    env = SnakeEnv(render_mode=True)
    agent = DQNAgent(state_size=7, action_size=3)
    agent.load(agent_path)
    agent.epsilon = 0.0  # Disable exploration to act greedily

    for ep in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            action = agent.act(state)
            next_state, reward, done = env.step(action)
            state = next_state
            total_reward += reward
            pygame.time.delay(delay)

        print(f"Episode {ep+1} - Total Reward: {total_reward}")

    pygame.quit()




if __name__ == "__main__":
    
    
    mode = "train" # Change this to specify the task
    
    if mode == "play": # play the game manually
        game = SnakeGame()
        game.run()
        
    elif mode == "train": # train an AI model
        train_dqn()
        
    elif mode == "test":
        watch_trained_agent() # AI plays the game