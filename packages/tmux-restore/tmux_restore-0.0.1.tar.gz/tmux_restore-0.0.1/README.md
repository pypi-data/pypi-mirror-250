# tmux-restore

## Overview
Works with `tmux` to save and restore sessions across reboots.

## Features
- Save session windows, panes, and layouts automatically on detach/exit
- Automatically restore sessions on reboot

## To Do
- Save pane command/state

## Set Up
To install `tmux-restore`, clone the repository and run the following in the project root:
```bash
pip install -e .
```
Then edit your `.bashrc` file with the following content:
```bash
# colors...

# tmux-restore trigger
if ! tmux info &> /dev/null; then
    if ! tmux ls &> /dev/null; then
        python3 -m tmux-restore
    fi
fi

# aliases...
```
It is important that this is done above alias definition to avoid conflicts.
Add the following content to either where the other aliases are defined in your `.bashrc` file or to your `.bash_aliases` file:
```bash
tmux() {
    command tmux $*
    python3 -m tmux-restore save
}
```
This will ensure that your sessions save after you exit or detach from a `tmux` session. Restart your shell to apply the effects.
Your tmux sessions will now restore themselves across reboots!

## Usage
If you would like to save or restore your `tmux` sessions manually:
```bash
# Save
python3 -m tmux-restore save

# Restore
python3 -m tmux-restore
# OR
python3 -m tmux-restore restore
```
