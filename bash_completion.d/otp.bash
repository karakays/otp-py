#!/usr/bin/env bash

__otp_debug()
{
    if [[ -n ${BASH_COMP_DEBUG_FILE} ]]; then
        echo
        echo "args: $args"
        echo "count_args: $_count_args"
        echo "COMP_WORDS: ${COMP_WORDS[*]}"
        echo "COMP_CWORD: $COMP_CWORD"
        echo "COMP_LINE: $COMP_LINE"
        echo "CURRW: ${COMP_WORDS[COMP_CWORD]}"
        echo "cur: ${cur}"
        echo "prev: ${prev}"
        echo "cword: ${cword}"
        echo "words: ${words[*]}"
    fi
}

_otp_completions()
{    
    local cur prev words cword
    _init_completion || return

    local args
    _count_args

    __otp_debug
 
    if ((args == 1)); then
        if [[ $cur == -* ]]; then
            COMPREPLY=($(compgen -W '--account --help --verbose --version' -- "$cur"))
            return
        fi

        if [[ $prev == -a || $prev == --account ]]; then
            COMPREPLY=( $(compgen -W "$(otp ls)" -- $cur) )
            return
        fi
        COMPREPLY=($(compgen -W \
            'add ls rm' -- "$cur"))
        return
    fi

    case ${words[1]} in
        add)
            if [[ $cur == -* ]]; then
                COMPREPLY=($(compgen -W '--issuer --secret --user --digits --algo --period' -- "$cur"))
            elif [[ $prev == --algo ]]; then
                COMPREPLY=($(compgen -W 'SHA1' -- "$cur"))
            elif [[ $prev == --digits ]]; then
                COMPREPLY=($(compgen -W '6 7 8' -- "$cur"))
            fi
            ;;
        rm)
            if [[ $cur == -* ]]; then
                COMPREPLY=($(compgen -W '--account' -- "$cur"))
            elif [[ $prev == --account ]]; then
                COMPREPLY=( $(compgen -W "$(otp ls | awk {'print $2 $3'})" -- $cur) )
                return
            fi
            ;;
    esac
} &&
    complete -F _otp_completions otp

