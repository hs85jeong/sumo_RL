import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
from sumo_rl import SumoEnvironment
from sumo_rl.util.gen_route import write_route_file
import traci

#from stable_baselines.common.policies import MlpPolicy
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import A2C

if __name__ == '__main__':
    DIR = './outputs/suwon'
    run = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    
    # multiprocess environment
    n_cpu = 4
    env = SubprocVecEnv([lambda: SumoEnvironment(net_file='nets/suwon_3nd/osm.net.xml',
                                        route_file='nets/suwon_3nd/osm.passenger1.trips.xml',
                                        out_csv_name='outputs/suwon/a2c',
                                        single_agent=True,
                                        use_gui=False,
                                        num_seconds=4000,
                                        max_depart_delay=20) for _ in range(n_cpu)])

    while True:
        model = A2C("MlpPolicy", env, verbose=1, n_steps=100)

        run = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        try:
            model.load("a2c_suwon")
            print(f'use model previous one. run_count = {run}')
        except FileNotFoundError:
            print(f'model is not loaded before.')

        try:
            model.learn(total_timesteps=4000)
        except:
            print ("ERROR")
            pass
        model.save("a2c_suwon")
