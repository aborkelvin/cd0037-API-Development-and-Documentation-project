# Backend - Trivia APP

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) if you don't have it installed.

2. **PIP Dependencies** - Install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```


### Database Setup

Ensure postgres is running then create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

To run the server, execute this from inside the `/backend` directory in terminal:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Done with setting up, return to the main [Api documentation](../README.md) here
