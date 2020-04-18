This plugin will launch a notification when a long running command finishes
and terminal is not active.

It uses VTE's special sequence which is sent when shell prints the prompt. It
depends on https://github.com/GNOME/vte/blob/vte-0-58/src/vte.sh (which has to
be added to /etc/profile.d) and you need to ensure `__vte_prompt_command` is
executed on `PROMPT_COMMAND` in Bash or in `precmd_functions` in Zsh.

Code is written in Hy and generated to Python3.
