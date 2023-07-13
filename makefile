all: pull structure preprocess
.PHONY: pull

pull:
	@echo "Pulling grants from NSF api ..."
	bash ./scripts/nsf_data_pull.sh "01/01/1970" "12/31/2022" "id,agency,startDate,expDate,pdPIName,poName,abstractText,title,publicationResearch,publicationConference,piFirstName,piMiddleInitial,piLastName,piEmail"

structure:
	@echo "Structuring data ..."
	python ./scripts/structure_data.py

preprocess:
	@echo "Preprocessing data ..."
	python ./scripts/preprocess_data.py


