#!/bin/bash

SUCCESS=0
FAILURE=1
PORT=${1:-5000}

COMMANDS=(  "python3 -m venv venv"
            "source venv/bin/activate"
            "python3 -m pip install --upgrade pip"
            "pip install -r requirements.txt"
            "python3 app.py --port ${PORT}" )

for COMMAND in "${COMMANDS[@]}"
do
    echo -e "\n[INFO]: Executing command: [${COMMAND}] ..."
    ${COMMAND}
    if [ $? -ne "${SUCCESS}" ]
    then
        echo -e "[ERROR]: Error occoured in executing command: [${COMMAND}]\n"
        exit ${FAILURE}
    fi
done
