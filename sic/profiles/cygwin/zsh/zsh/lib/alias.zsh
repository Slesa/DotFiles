alias -g L=' | less'
alias -g M=' | less'
alias -g H=' | head'
alias -g T=' | tail'
alias -g G=' | grep'

alias cd..='cd ..'
alias cd/='cd /'

alias 1='cd -'
alias 2='cd +2'
alias 3='cd +3'
alias 4='cd +4'
alias 5='cd +5'
alias 6='cd +6'
alias 7='cd +7'
alias 8='cd +8'
alias 9='cd +9'
alias di='dirs -v'
alias dirs='dirs -v'

alias md='mkdir -p'
alias rd='rmdir'
alias wgets='wget --spider --server-response'
alias upload='~/bin/upload.sh'

alias ls='ls --color=auto -l --all --human-readable --group-directories'
alias dir='ls'

# Also done by Ctrl + L.
alias cls='echo -ne "\033c"'
alias g='git'

alias sudo='cygstart --action=runas'

alias gem='gem.bat'
alias rake='rake.bat'
alias irb='irb.bat'
# bundle conflicts with the git-bundle auto-alias, so define a second alias.
alias bundle='bundle.bat'
alias bun='nocorrect bundle.bat'
alias bex='nocorrect bundle.bat exec'
