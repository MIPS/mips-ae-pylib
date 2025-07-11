import atlasexplorer
import locale


def test_singlecore():
    locale.setlocale(locale.LC_ALL, "")
    # example use of AtlasExplorer library,
    # this assumes that user has ran the script with the "configure" arg
    # Create an instance of the class
    aeinst = atlasexplorer.AtlasExplorer(
        "de627017-532c-4cef-adff-5c9c444440df",
        "threading-mode-2",
        "us-west-2",
        verbose=True,
    )
    # create a new experiment
    experiment = atlasexplorer.Experiment("myexperiments", aeinst, verbose=True)
    # add a workload to the experiment
    experiment.addWorkload("resources/mandelbrot_rv64_O0.elf")
    # experiment.addWorkload("resources/memcpy_rv64.elf")
    # set the core type for the experiment
    experiment.setCore("I8500")
    # run an experiment
    experiment.run()

    total_cycles = experiment.getSummary().getTotalCycles()
    assert total_cycles == 253629, "Total Cycles should be 253629"
