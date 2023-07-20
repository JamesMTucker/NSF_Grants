all: delete pull create_db populate_db preprocess
.PHONY: all

ENV_NAME=nsf
PYTHON=conda run -n $(ENV_NAME) python

delete:
	@echo "Deleting database ..."
	rm -f ./data/nsf.db

create_env:
	@echo "Creating environment ..."
	conda create -n $(ENV_NAME) python=3.11

pull:
	@echo "Pulling grants from NSF api ..."
	# bash ./scripts/nsf_data_pull.sh "01/01/1970" "12/31/2030" "id,agency,date,startDate,expDate,pdPIName,poName,abstractText,title,publicationResearch,publicationConference,piFirstName,piMiddleInitial,piLastName,piEmail"

create_db:
	@echo "Creating database ..."
	$(PYTHON) ./scripts/create_db.py

preprocess:
	@echo "Preprocessing data ..."
	# $(PYTHON) ./scripts/preprocess.py

populate_db:
	@echo "Populating the database ..."
	# $(PYTHON) ./scripts/populate_db.py

clean:
	@echo "Cleaning up ..."
	conda env remove -n $(ENV_NAME)

