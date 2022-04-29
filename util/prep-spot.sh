#!/bin/bash

CONDA_BASE=$(conda info --base)
. $CONDA_BASE/etc/profile.d/conda.sh

xdir=$(dirname $0)
SPOT_DIR=$xdir/../../

threshold=$2

while read m; do
    conda activate venv_spotrna_2d
    python $xdir/prob2cst.py $SPOT_DIR/predictions/SPOT-RNA-2D/$m.prob $SPOT_DIR/input_features/$m $xdir/../RNAFOLD/$m.fn $threshold > $m/$m.cst
    conda deactivate
    cd $m
    echo "-cst_file $m.cst" >> flags
    echo "-output_lores_silent_file" >> flags
    sed -i 's/true/false/g' flags
    conda activate py2_spot
    rosetta_submit.py README_FARFAR FARFAR 10 16
    conda deactivate
    cd ..
done <$1
