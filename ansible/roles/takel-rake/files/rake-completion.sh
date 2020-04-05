#!/usr/bin/env bash

# Bash completion for Rake
# Based on https://gist.github.com/turadg/840663

export COMP_WORDBREAKS=${COMP_WORDBREAKS/\:/}

function _rakecomplete() {

  # Error if no Rakefile
  if [[ ! -e Rakefile ]]; then
    return 1
  fi

  local tasks=$(rake --tasks --silent | awk '{print $2}')
  COMPREPLY=($(compgen -W "${tasks}" -- ${COMP_WORDS[COMP_CWORD]}))
  return 0

}

complete -o default -o nospace -F _rakecomplete rake
