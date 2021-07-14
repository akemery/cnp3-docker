#!/bin/bash

# In this exercice your have to create the file $1 in you home directory

verify_file(){
    if [ -f "$1" ]; then
        echo "Success";
    else
        echo "Failed";
    fi  
}

verify_file $1
