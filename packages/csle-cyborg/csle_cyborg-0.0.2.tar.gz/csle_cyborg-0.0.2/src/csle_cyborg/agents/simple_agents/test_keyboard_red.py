from csle_cyborg.main import Main
import inspect
from csle_cyborg.agents.simple_agents.blue_monitor_agent import BlueMonitorAgent
from csle_cyborg.agents.simple_agents.keyboard_agent import KeyboardAgent
from csle_cyborg.agents.wrappers.red_table_wrapper import RedTableWrapper

if __name__ == "__main__":
    print("Setup")
    path = str(inspect.getfile(Main))
    path = path[:-7] + '/Shared/Scenarios/Scenario1b.yaml'

    cyborg = RedTableWrapper(env=Main(path, 'sim', agents={'Blue': BlueMonitorAgent}), output_mode='table')
    agent_name = 'Red'

    results = cyborg.reset(agent=agent_name)
    observation = results.observation
    action_space = results.action_space

    agent = KeyboardAgent()

    reward = 0
    done = False
    while True:
        action = agent.get_action(observation, action_space)
        results = cyborg.step(agent=agent_name, action=action)

        reward += results.reward
        observation = results.observation
        action_space = results.action_space
        if done:
            print(f"Game Over. Total reward: {reward}")
            break
