# Backlog Stats

## How to run

First, you need some IGBD API keys. See [the docs](https://api-docs.igdb.com/#getting-started) for creating them.

Once you have those keys, create a `.env` file in the `backlogstats_back` subfolder with the following structure

```
SECRET_KEY=secretKey
IGDB_API_CLIENT_ID=abc123
IGDB_API_CLIENT_SECRET=abc123
IGDB_API_ACCESS_TOKEN=abc123
```

Replace `abc123` with your own keys. And `secretKey` with a randomly generated key using [this online generator](https://djecrety.ir/)

Then, you must install the project dependencies

```
pip install -r requirements.txt
```

Create the migrations, if any

```
python manage.py makemigrations
```

Apply all migrations

```
python manage.py migrate
```

And finally, create an admin user

```
python manage.py createsuperuser
```

Now you should be able to run the project
```
python manage.py runserver
```

### First steps

You should GET to `/igdb/update_genres/` and `/igdb/update_platforms` to populate both Genre and Platforms tables.