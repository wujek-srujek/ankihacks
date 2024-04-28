#!/usr/bin/env bash

# Expands verbs to multiple notes, one for each form.
#
# Adds tags for: the tense, the person, plurality, and if the form is common.
# Input file consists of multiple lines with the following syntax:
# <verb in infinitive>;<vorb forms>;<tense>
# For example:
# ser;sou és é somos sois são;presente
#
# Note: each verb form corresponds to its pronoun (see `pronouns` below).

set -e

if [ $# -ne 1 ]; then
  echo "Usage: $0 <input file>"
  exit 1
fi

pronouns=(eu tu ele/você nós vós eles)

function generate_note() {
  echo -e "\"($tense)\n\n$question\n\n($pronoun)\";${forms[$i]};${tags[@]}"
}

cat "$1" | while read line; do
  IFS=';' read -r question answer tense <<< "$line"
  read -a forms <<< "$answer"

  for i in "${!forms[@]}"; do
    tags_base=($tense)
    if [ $i -le 2 ]; then
      tags_base+=(singular)
    else
      tags_base+=(plural)
    fi

    if [ $i != 1 -a $i != 4 ]; then
      tags_base+=(comum)
    fi

    if [ $i == 2 ]; then
      for pronoun in ele você; do
        tags=("${tags_base[@]}" $pronoun)
        generate_note
      done
    else
      pronoun="${pronouns[$i]}"
      tags=("${tags_base[@]}" $pronoun)
      generate_note
    fi
  done
done
