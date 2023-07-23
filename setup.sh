#!/bin/bash

# Array of programs to check
programs=("docker" "jq" "gcc" "make" "wget" "libwww-perl" "docker")

# Function to check if program is installed
check_program() {
    if ! command -v $1 &> /dev/null
    then
        read -p "$1 is not installed. Would you like to install it? (y/n) " answer
        case ${answer:0:1} in
            y|Y )
                if [[ "$1" == "jq" || "$1" == "gcc" || "$1" == "make" || "$1" == "wget" || "$1" == "libwww-perl" ]]
                then
                    sudo apt-get install $1
                elif [[ "$1" == "docker" ]]
                then
                    sudo apt-get install docker.io
                else
                    echo "$1 not recognized"
                fi
            ;;
            * )
                echo "$1 will not be installed"
                exit 1
            ;;
        esac
    fi
}

if [[ -z "$1" ]]; then
    echo "Use -h for help"
    exit 1
fi

while [ ! -z "$1" ]; do
    case "$1" in
        -l|--local)
            for program in "${programs[@]}"; do
                check_program $program
            done
            make
            ;;
        -d|--docker)
            docker build -t nsf .
            docker run -it --rm -v $(pwd)/data:/data nsf
            ;;
        -h|--help)
            echo "Usage: ./setup.sh [OPTION]"
            echo "Options:"
            echo "  -l, --local     Run locally"
            echo "  -d, --docker    Run in docker container"
            echo "  -h, --help      Display this help message"
            exit 0
            ;;
        *)
            echo "Use -h for help"
            exit 1
            ;;
    esac
    shift
done