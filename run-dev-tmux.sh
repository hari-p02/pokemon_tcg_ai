#!/bin/bash

# Start a new tmux session named "pokemon-ai"
tmux new-session -d -s pokemon-ai

# Bind the "x" key to kill the session
tmux bind-key x kill-session

# Split the window horizontally
tmux split-window -h

# Adjust the size of the panes
tmux resize-pane -t 0 -x 50%  # Make both panes equal width

tmux select-pane -t 1
tmux send-keys "cd $(pwd)/client && npm run dev" C-m

# Enable mouse mode for easy pane switching
tmux setw -g mouse on

# Set window title
tmux set-option -g set-titles on
tmux set-option -g set-titles-string "Pokemon AI"

# Increase scrollback buffer
tmux set-option -g history-limit 50000

# Attach to the session only if in iTerm2
if [ "$TERM_PROGRAM" = "iTerm.app" ]; then
  tmux -CC attach-session -t pokemon-ai
else
  tmux attach-session -t pokemon-ai
fi 