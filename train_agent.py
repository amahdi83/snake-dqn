import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import numpy as np
from snake_env import SnakeEnv

# Simple fully connected Q-network
class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            # nn.Linear(hidden_size, hidden_size),
            # nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100_000)
        self.gamma = 0.9
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.lr = 0.001
        self.batch_size = 64

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = QNetwork(state_size, 128, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randint(0, self.action_size - 1)
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            act_values = self.model(state)
        return torch.argmax(act_values).item()

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, targets = [], []

        for state, action, reward, next_state, done in batch:
            state_tensor = torch.tensor(state, dtype=torch.float32).to(self.device)
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32).to(self.device)

            target = self.model(state_tensor).clone().detach()
            if done:
                target[action] = reward
            else:
                next_q_values = self.model(next_state_tensor)
                target[action] = reward + self.gamma * torch.max(next_q_values).item()

            states.append(state_tensor)
            targets.append(target)

        states_tensor = torch.stack(states)
        targets_tensor = torch.stack(targets)

        output = self.model(states_tensor)
        loss = self.loss_fn(output, targets_tensor)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def save(self, filepath="dqn_snake.pth"):
        torch.save({
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "epsilon": self.epsilon
        }, filepath)
        print(f"Model saved to {filepath}")

    def load(self, filepath="dqn_snake.pth"):
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.epsilon = checkpoint.get("epsilon", 0.1)
        self.model.eval()  # Switch to evaluation mode
        print(f"Model loaded from {filepath}")