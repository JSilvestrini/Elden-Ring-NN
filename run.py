from stable_baselines3 import PPO
from gymnasium.wrappers.gray_scale_observation import GrayScaleObservation
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
import os
import sys
import er_environment

MAX_MEMORY = 2048
BATCH_SIZE = 512
LEARNING_RATE = 0.0002
CHECKPOINT_DIR = './model/'
LOG_DIR = './logs/'

class CallBack(BaseCallback):
    def __init__(self, freq, path, verbose=1):
        super(CallBack, self).__init__(verbose)
        self.freq = freq
        self.path = path

    def _init_callback(self):
        if self.path is not None:
            os.makedirs(self.path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.freq == 0:
            model_path = os.path.join(self.path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True

def train_ppo(n_train):
    callback = CallBack(freq=10000, path=CHECKPOINT_DIR)
    env = er_environment.EldenRing(action_space=1)
    #print(env.observation_space.shape)
    env = GrayScaleObservation(env, keep_dim=True)
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, 4, channels_order='last')
    model = PPO('CnnPolicy', env, verbose=1, learning_rate=LEARNING_RATE, n_steps=1024)
    model.learn(total_timesteps=n_train*10000, callback=callback)

if __name__ == "__main__":
    n_train = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    train_ppo(n_train)