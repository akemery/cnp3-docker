#!/bin/bash

# In this exercice your have add a text a end of the following file

verify_append_to_file(){
    r=`tail -n 1 $1`
    if [ "$r" = "$2" ]; then
        echo "Success";
    else
        echo "Failed";
    fi  
}

verify_append_to_file $1 $2
