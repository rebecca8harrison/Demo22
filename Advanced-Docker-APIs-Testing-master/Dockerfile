# start from the official Python 3.8 image, slim version as we don't need any binary dependencies
FROM python:3.8-slim

# install the pipenv tool, so we can install our application depedencies
RUN pip install pipenv

# create directory /app and cd into it
WORKDIR /app

# copy the dependency specification into the image, so we can install the dependencies
COPY Pipfile Pipfile.lock /app/

# install dependencies
RUN pipenv install

EXPOSE 8000

# we copy the application code over next
# the application code changes more frequently than the dependencies
# so we can avoid reinstalling the dependencies by running this copy command afterwards
COPY python/ /app/python/

# run the application when the container runs, listening for all traffic on port 8000
ENTRYPOINT ["pipenv", "run", "uvicorn", "python.main:app", "--host", "0.0.0.0", "--port", "8000"]

# we would run this container with `docker run -p8000:8000 container-tag-or-id`