DC = docker compose
FILE = infra/project.yaml
EXEC = docker exec -it
ENV = --env-file .env
LOGS = docker logs



URL_FILE_MAIN = app/bot.py
test = app/main.py



.PHONY: containers
containers:
	${DC} -f ${FILE} ${ENV} up -d --build






.PHONY: run
run:
	python ${URL_FILE_MAIN}

URL_FILE_MAIN = app/bot.py

.PHONY: run-test
run-test:
	python ${test}