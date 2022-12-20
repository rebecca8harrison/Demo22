Supporting materials for Data Science Bootcamp - Docker, APIs and Testing

# Contents

Run `pipenv install --dev` before starting.

This repository provides base code to run a machine learning model API server.

# Run the Server (Development)

To run the server from the root of the project: `pipenv run uvicorn python.main:app --reload`.

- Server will start on [http://localhost:8000](http://localhost:8000)
- Documentation will be served at [http://localhost:8000/docs](http://localhost:8000/docs)
- The `--reload` means that the server will automatically pick up changes you make.

# Build the Docker Container

- `docker build -t ml-model .` - build the [Dockerfile](Dockerfile)

# Run the Docker Container

- `docker run -p8000:8000 ml-model` - run a container based on the image we just built (and tagged as `ml-model`)
