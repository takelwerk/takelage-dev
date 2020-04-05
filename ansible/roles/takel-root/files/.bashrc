# .bashrc

# User specific aliases and functions
alias l='ls -la'

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

# Add /usr/local/bin to PATH
PATH=$PATH:/usr/local/bin

# Set default encoding
export LC_ALL=en_US.UTF-8
export LANG=en_US.utf8

# Add autocompletion
source <(gopass completion bash)
source <(tau completion bash)
