#!/bin/bash
git config --global user.email "bhickm13@wgu.edu"
git config --global user.name "bob-student-DA"
git config --global credential.helper store
git config --global pull.rebase false

#---Conda---
if [ ! -d "$HOME/miniconda3" ]; then
   curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash miniconda.sh -b -p $HOME/miniconda3
fi

source $HOME/miniconda3/etc/profile.d/conda.sh

conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

if ! conda env list | grep -q fastapi; then
   conda env create -f environment.yml
fi

conda activate fastapi
echo "Environment ready. Python: $(which python)"
