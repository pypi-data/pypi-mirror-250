from csle_cyborg.main import Main
import inspect


# Set up CybORG
print("Setup")
path = str(inspect.getfile(Main))
path = path[:-7] + '/Shared/Scenarios/Scenario1KeyboardRed.yaml' # Change this to pick your agents
cyborg = Main(path, 'sim')

for i in range(1):
    print(f"Game: {i}")
    cyborg.start(1000)
    cyborg.reset()

