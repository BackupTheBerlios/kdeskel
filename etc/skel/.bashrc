# /etc/skel/.bashrc:
# $Header: /home/xubuntu/berlios_backup/github/tmp-cvs/kdeskel/Repository/etc/skel/.bashrc,v 1.1 2004/10/27 09:16:31 hds Exp $
# Modified 20041025 by hds

# This file is sourced by all *interactive* bash shells on startup.  This
# file *should generate no output* or it will break the scp and rcp commands.

# colors for ls, etc.
eval `dircolors -b /etc/DIR_COLORS`
alias d="ls --color"
alias ls="ls --color=auto"
alias ll="ls --color -l"

# Change the window title of X terminals 
case $TERM in
	xterm*|rxvt|Eterm|eterm)
		PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\007"'
		;;
	screen)
		PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\033\\"'
		;;
esac

##uncomment the following to activate bash-completion: (uncommented by hds)
[ -f /etc/profile.d/bash-completion ] && source /etc/profile.d/bash-completion
