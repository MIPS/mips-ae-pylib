import atlasexplorer
import sys
import locale

# Set locale for number formatting
locale.setlocale(locale.LC_ALL, "")

# example use of AtlasExplorer library,
# this assumes that user has ran the script with the "configure" arg
# Create an instance of the class
aeinst = atlasexplorer.AtlasExplorer(verbose=True)
# aeinst.setRootExperimentDirectory("myexperiments")

experiment = atlasexplorer.Experiment("myexperiments", aeinst, verbose=True)

# run an experiment with your elf / core selelection
# returns exp sub dir name

# experiment.createExperiment(
#    ["resources/mandelbrot_rv64_O0.elf", "resources/memcpy_rv64.elf"], "shogun_2t"
# )
experiment.createExperiment(["resources/mandelbrot_rv64_O0.elf"], "I8500")
# print("experiment dir: " + experiment.getRoot())
print(
    "total cycles: "
    + locale.format_string(
        "%d", experiment.getSummary().getTotalCycles(), grouping=True
    )
)
print(
    "total instructions: "
    + locale.format_string(
        "%d", experiment.getSummary().getTotalInstructions(), grouping=True
    )
)

""" 
experiment2 = aeinst.getExperiment(experiment.getRoot())
if experiment2 is None:
    print("error getting experiment! Check your setup")
    sys.exit(1)
print("experiment2 dir: " + experiment2.getRoot())
print(
    "experiment2 total cycles: "
    + locale.format_string(
        "%d", experiment2.getSummary().getTotalCycles(), grouping=True
    )
)
print(
    "experiment2 total instructions: "
    + locale.format_string(
        "%d", experiment2.getSummary().getTotalInstructions(), grouping=True
    )
)


list = experiment2.getSummary().getMetricKeys()
print("\nAll Metric Key in the experiment summary:")
for item in list:
    print(item)

print("\nCache Metrics in the experiment summary:")
experiment2.getSummary().printMetrics(".*Cache.*")

cacheHits = experiment2.getSummary().getMetricValue(
    "Level 1 Instruction Cache (L1ICache) Hits"
)
print("\nFetch a single metric key by name:")
print(
    "  Level 1 Instruction Cache (L1ICache) Hits: "
    + locale.format_string("%d", cacheHits, grouping=True)
)
 """
