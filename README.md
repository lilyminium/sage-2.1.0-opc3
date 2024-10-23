# sage-2.1.0-opc3

This directory contains materials and scripts used to carry out a re-fit of Sage 2.1.0 with OPC3 water.

**Note: since this fit was started, we have uncovered several issues with Evaluator. One was fixed in 0.4.10 (https://github.com/openforcefield/openff-evaluator/issues/575); we're still troubleshooting the other. We would recommend *not* using the environment in this repo to run further fits until everything is fixed.**

## environments

The environments used in fitting and benchmarking.

## data

The dataset was copied from the Sage 2.0 fit. No additional curation was conducted.


## fit

The directory used to run the vdW re-fit to condensed-phase properties.

Note: to run this and avoid errors about daemons you may need to set the following options in ``~/.config/dask/distributed.yaml``:

```
distributed:

    worker:
        daemon: False

    comm:
        timeouts:
            connect: 10s
            tcp: 30s

    deploy:
        lost-worker-timeout: 15s
```

I also set the following options on the Iris cluster in ``~/.config/dask/jobqueue.yaml``:


```
  slurm:
    name: dask-worker

    # Dask worker options
    cores: null                 # Total number of cores per job
    memory: null                # Total amount of memory per job
    processes: null                # Number of Python processes per job

    interface: null             # Network interface to use like eth0 or ib0
    death-timeout: 60           # Number of seconds to wait if a worker can not find a scheduler
    local-directory: null       # Location of fast local storage like /scratch or $TMPDIR
    shared-temp-directory: null       # Shared directory currently used to dump temporary security objects for workers
    extra: null                 # deprecated: use worker-extra-args
    worker-extra-args: []       # Additional arguments to pass to `dask-worker`

    # SLURM resource manager options
    shebang: "#!/usr/bin/env bash"
    queue: "gpu"
    project: null
    walltime: '00:30:00'
    env-extra: null
    job-script-prologue: ["nvidia-smi"]
    job-cpu: null
    job-mem: null
    job-extra: null
    job-extra-directives: []
    log-directory: "worker-logs"

    # Scheduler options
    scheduler-options: {}
```
