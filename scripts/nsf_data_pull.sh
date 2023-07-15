#!/bin/bash

# Check the arguments

# arg 1: begin date
if [ ! -z "$1" ]; then
    begin_date=$1
else
    echo "Please provide a begin date"
    exit 1
fi

# arg 2: end date
if [ ! -z "$2" ]; then
    end_date=$2
else
    echo "Please provide an end date"
    exit 1
fi

# arg 3: fields
if [ ! -z "$3" ]; then
    fields=$3
    # check if the fields are comma separated
    if [[ $fields != *,* ]]; then
        echo "Please provide fields as comma separated values"
        exit 1
    fi
else
    echo "Please provide fields: see API docs https://resources.research.gov/common/webapi/awardapisearch-v1.htm"
    exit 1
fi

# Create data directory
if [ ! -d "data/nsf_grants" ]; then
    mkdir -p data/nsf_grants
fi

# Export variables for GNU Parallel
export begin_date
export end_date
export fields

# Define a function that will be run in parallel
process_url() {
    offset=$1
    base_url="http://api.nsf.gov/services/v1/awards.json?dateStart=${begin_date}&dateEnd=${end_date}&rpp=25&printFields=${fields}"
    url="${base_url}&offset=${offset}"
    response=$(GET "$url")

    if [ $? -ne 0 ]; then
        echo "Error fetching data at ${offset}"
        return 1
    fi

    num_results=$(echo "$response" | jq '.response.award | length')
    echo "$response" | iconv -f utf-8 -t utf-8 > "./data/nsf_grants/nsf_${offset}.json"

    if (( num_results < 25 )); then
        echo "Fetched $num_results records in $offset"
        return 0
    else
        echo "Fetched 25 records in $offset"
    fi
}
export -f process_url

# Use GNU Parallel to run the function in parallel
seq 1 25 400000 | parallel process_url