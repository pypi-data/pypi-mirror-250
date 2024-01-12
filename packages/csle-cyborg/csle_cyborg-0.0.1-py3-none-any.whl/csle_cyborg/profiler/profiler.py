import inspect
from csle_cyborg.main import Main

# for visualisation of code profile:
# python -m cProfile -o profile.pstats profiler.py
# gprof2dot -f pstats profile.pstats | dot -Tpng -o output.png && eog output.png
# from CybORG.CybORG import AWSConfig


def run():
    aws = True
    if not aws:
        c = Main(path, 'sim')
    else:
        raise ValueError("Aws not supported")
    try:
        for i in range(1):
            c.start(50)
            # c.reset()
    finally:
        c.shutdown(teardown=True)
path = str(inspect.getfile(Main))
path = path[:-7] + '/Shared/Scenarios/Scenario1.yaml'
# cProfile.run("run()", sort='cumtime')
run()



