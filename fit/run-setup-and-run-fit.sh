#!/usr/bin/env bash
#SBATCH -J sage-2.1-opc3
#SBATCH -p standard
#SBATCH -t 96:00:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --account dmobley_lab
#SBATCH --output slurm-%x.%A.out

PORT=8002


conda activate sage-2.1.0-opc3

# write force field
python setup-forcefield.py --input "openff-2.1.0.offxml" --water "opc3.offxml"

# write client options
python setup-options.py --port $PORT

# run fit
python execute-fit-slurm-distributed.py             \
    --port              $PORT                       \
    --n-min-workers     1                           \
    --n-max-workers     24                          \
    --memory-per-worker 8                           \
    --walltime          "24:00:00"                  \
    --queue             "free-gpu"                  \
    --conda-env         "sage-2.1.0-opc3"
