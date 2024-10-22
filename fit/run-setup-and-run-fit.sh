#!/usr/bin/env bash
#SBATCH -J sage-2.1-opc3
#SBATCH -p cpu
#SBATCH -t 96:00:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --output slurm-%x.%A.out

PORT=8002

source ~/.bashrc
conda activate sage-2.1.0-opc3

# write force field
# python setup-forcefield.py --input "openff-2.1.0.offxml" --water "opc3.offxml"

# write client options
# python setup-options.py --port $PORT

# run fit
python execute-fit-slurm-distributed.py             \
    --port              $PORT                       \
    --n-min-workers     1                           \
    --n-max-workers     60                          \
    --memory-per-worker 8                           \
    --walltime          "08:00:00"                  \
    --queue             "gpu"                       \
    --conda-env         "sage-2.1.0-opc3"           \
    --extra-script-option "--gpus-per-task=1"              # note: this is Iris specific
