# Magic Mirror
A fun taling mirror halloween project 

## Downloading

in a terminal, run `git clone [repository link]`, where the repository link can by clicking the 'Code' button and copying the HTTPS address.

## Before running

Populate the 'rules.yml' file with your Google Genai API key in the `api_key` section, and the instructions for the chatbot to follow in the `rules` section.

## Running the program

Run `./setup.sh` to initialize a virtual environment and download dependancies. If you are unable to run the file, you can grant it priviledge to do so by running `chmod +x setup.sh`.

You can start the program by then running `./run.sh`. If you cannot run the program, you can give it permission with `chmod +x run.sh`.