import inspect
from csle_cyborg.main import Main
from csle_cyborg.agents.simple_agents.meander import RedMeanderAgent
from csle_cyborg.agents.wrappers.blue_table_wrapper import BlueTableWrapper
from csle_cyborg.agents.wrappers.enum_action_wrapper import EnumActionWrapper
from csle_cyborg.agents.wrappers.open_ai_gym_wrapper import OpenAIGymWrapper
from csle_cyborg.agents.wrappers.reduce_action_space_wrapper import ReduceActionSpaceWrapper


def run():
    path = str(inspect.getfile(Main))
    path = path[:-7] + '/Shared/Scenarios/Scenario1b.yaml'
    red_agent = RedMeanderAgent
    agent_name = 'Red'
    c = OpenAIGymWrapper(agent_name,
                              EnumActionWrapper(
                                  ReduceActionSpaceWrapper(
                                      BlueTableWrapper(
                                          Main(path, 'sim', agents={'Red': red_agent}),
                                          output_mode='vector'))))
    for i in range(100):
        for i in range(50):
            c.step()
        c.reset()

# cProfile.run("run()", sort='cumtime')
run()

#cyborg = DummyVecEnv([lambda: cyborg])
# num_cpu = 4
# cyborg = SubprocVecEnv([make_blue_env(red_agent) for i in range(num_cpu)])
