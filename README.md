# National Science Foundation Grants

This repository contains code to extract data on grants awarded by the [National Science Foundation](https://resources.research.gov/common/webapi/awardapisearch-v1.htm) (NSF) from 1970 to 2023. If you are working on a Linux machine, you can run the code locally. Otherwise, you can run the code in a Docker container.

To run the code locally, you will need to run `setup.sh` with the `--local` flag. This will install the necessary packages and download the data. You can then run `make` to extract the data.

To run the code in a Docker container, you will need to run `setup.sh` with the `--docker` flag. This will build the Docker image and download the data. Once the image is built and the data downloaded, connect to the docker instance.

## NSF API

The default method extracts grant data for the for the following parameters:

  * startDate = 01/01/1970
  * expDate = 12/31/2023
  * Print fields: `id`, `agency`, `date`, `startDate`, `expDate`, `pdPIName`, `poName`, `abstractText`, `title`, `publicationResearch`, `publicationConference`, `piFirstName`, `piMiddleInitial`, `piLastName`, `piEmail`
  
Change these parameters in the `Makefile` to extract different data.

