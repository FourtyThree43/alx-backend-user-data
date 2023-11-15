#!/usr/bin/env nu

# def fetch_fortune_quote [url] {
#   http get $url | get fortune
# }

# let quote = fetch_fortune_quote "http://yerkee.com/api/fortune/cookie" 

# echo $quote


# Check if folder names are provided as command-line arguments
if $(echo $nu.env.args | empty?) == $true {
    echo "Usage: script.nu folder_name1 folder_name2 ..."
    exit
}

# # Loop over folder name arguments
# for folder_name in $nu.env.args {
#     mkdir $folder_name
# }
