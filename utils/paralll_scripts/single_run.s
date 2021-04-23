#!/bin/bash
#SBATCH --job-name=parse
#SBATCH --open-mode=append
#SBATCH --output=./output/%j_%x.out
#SBATCH --error=./output/%j_%x.err
#SBATCH --export=ALL
#SBATCH --cpus-per-task=1
#SBATCH --mem=80G
#SBATCH --time=1-0
#SBATCH --mail-type=END
#SBATCH --mail-user=ayl316@nyu.edu
#SBATCH -c 4

singularity exec --overlay $HOME/overlay-25GB-500K.ext3:ro /scratch/work/public/singularity/ubuntu-20.04.1.sif  /bin/bash -c "
source /ext3/env.sh
conda activate ttml
python ./create_jobs.py 1
"
