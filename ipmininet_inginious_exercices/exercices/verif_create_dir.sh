#!/bin/bash

# In this exercise your have to create the directory $1 in you $HOME directory

verify_dir(){
    if [ -d "$1" ]; then
        echo "Success";
    else
        echo "Failed";
    fi  
}

verify_dir $1
