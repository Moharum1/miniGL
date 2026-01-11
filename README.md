# MINI-GL
Is a minimal implementation for a RAG model to answer question of OpenGL 4.0 API

## Requirement
- Python 3.8 or later
- It's advisable to run the code on a new Virtual conda Environment but it can also work on the Machine python version with no problem

### Installation
- Copy the `.env.example` file and edit the empty constants with your own values

### Run the server
- The app runs on uvicorn server a fast server that is written in rust in order to run our fast api code on it we use the below command
`python3 -m uvicorn main:app --reload`