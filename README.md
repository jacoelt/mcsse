# Minecraft Server Explorer

Website is available at https://minecraft-server-explorer.onrender.com


## Why?
Most Minecraft server listing available online are used as voting platform for servers, and list servers by popularity.
They usually offer very little capabilities in terms of search for players.

This project aims to get lists of servers from various publicly available websites and provide actually
usable search for players looking for their next adventure.

## What?
The repository is subdivised in back and front repositories, each handling their respective part of the project.

The frontend provides a React single-page application, making api calls to the backend to get the list of servers.

The backend provides a Django-Ninja api to search the database for servers, as well as a Django command to fetch data
from various Minecraft lists.

Only one website fetcher is implemented for now.

## How?
If you want to run this project locally, here's what you need to do

### Backend
Copy `.env.dist` file into `.env`, filling in the values you need

```shell
cd back
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

### Frontend
Copy `.env.dist` file into `.env`, filling in the values you need

```shell
cd front
npm install
npm run dev
```
