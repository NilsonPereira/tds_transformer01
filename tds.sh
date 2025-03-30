# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/nmlabuser/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/nmlabuser/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/nmlabuser/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/nmlabuser/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate tango
python transformer_tds.py transformer01

