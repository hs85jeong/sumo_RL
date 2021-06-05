import gym
from stable_baselines3.dqn.dqn import DQN
import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
from sumo_rl import SumoEnvironment
import traci


if __name__ == '__main__':
    DIR = './outputs/suwon_dqn'

    env = SumoEnvironment(net_file='nets/suwon_3nd/osm.net.xml',
                                    route_file='nets/suwon_3nd/osm.passenger1.trips.xml',
                                    out_csv_name='outputs/suwon_dqn/dqn',
                                    single_agent=True,
                                    use_gui=False,
                                    num_seconds=4000,
                                    max_depart_delay=0)

    while True:
        model = DQN(
            env=env,
            policy="MlpPolicy",
            learning_rate=0.01,
            learning_starts=0,
            train_freq=1,
            target_update_interval=100,
            exploration_initial_eps=0.05,
            exploration_final_eps=0.01,
            verbose=1
        )

        run = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        env.count = run

        try:
            model.load("dqn_suwon")
            print(f'use model previous one. run_count = {run}')
        except FileNotFoundError:
            print(f'model is not loaded before.')

        try:
            model.learn(total_timesteps=4000)
        except:
            print ("ERROR")
            pass
        model.save("dqn_suwon")
