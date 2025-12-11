#!/bin/bash

SUCCESS=0
FAILURE=1
PORT=${1:-5000}

COMMANDS=(  "rm -rf venv"
            "python3 -m venv venv"
            "source venv/bin/activate"
            # "python3 -m pip install --upgrade pip"
            "pip install -r requirements.txt" )

for COMMAND in "${COMMANDS[@]}"
do
    echo -e "\n[INFO]: Executing command: [${COMMAND}] ..."
    ${COMMAND}
    if [ $? -ne "${SUCCESS}" ]
    then
        echo -e "[ERROR]: Error occoured in executing command: [${COMMAND}]\n"
        exit ${FAILURE}
    fi
    echo -e "[INFO]: Execution complete!!!"
done

mkdir -p data
kaggle datasets download -d rounakbanik/the-movies-dataset -p data
unzip -o data/the-movies-dataset.zip -d data
echo

python3 app.py --port ${PORT}
