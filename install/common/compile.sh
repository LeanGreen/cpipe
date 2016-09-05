#!/usr/bin/env bash
function compile {
# $1 is the directory to compile in
    pushd $1

    # If there's already a makefile, just run make
    if [[ -f Makefile ]]; then
        make
        make prefix="$1" install
        popd
        return 0
    fi

    # Ensure configure scripts are run
    if [[ -f  configure.ac ]]; then
        autoconf
    fi
    if [[ -f configure ]]; then
        yes | ./configure
    fi
    if [[ -f Configure ]]; then
        yes | ./Configure -d
    fi
    if [[ -f Makefile ]]; then
        make
        make prefix="$1" install
    else
        popd
        return 1
    fi

    popd
}