#!/bin/bash

# Set initial offset
offset=1

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

# print fields
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


# Set base URL
base_url="http://api.nsf.gov/services/v1/awards.json?dateStart=${begin_date}&dateEnd=${end_date}&rpp=25&printFields=${fields}"

while true; do
    # Build URL
    url="${base_url}&offset=${offset}"

    # create data directory
    if [ ! -d "data" ]; then
        mkdir data
    fi

    # Fetch data
    response=$(GET "$url")

    # validate response is 200
    if [ $? -ne 0 ]; then
        echo "Error fetching data at ${offset}"
        exit 1
    fi

    # Check if we got less than 25 results
    num_results=$(echo "$response" | jq '.response.award | length')

    if (( num_results < 25 )); then
        echo "$response" | iconv -f utf-8 -t utf-8 > "./data/nsf_year_${offset}.json"
        echo "Fetched $num_results records in $offset"
        exit 0
    else
        echo "$response" | iconv -f utf-8 -t utf-8 > "./data/nsf_year_${offset}.json"
        echo "Fetched 25 records in $offset"
    fi

    # Increment offset
    offset=$((offset + 25))
done
