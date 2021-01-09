# Flask Backend Test

## Load data to MongoDB

```bash
# run mongodb
docker pull mongo
docker run -d -p 27017:27017 -p 27018:27018 --name mongo mongo:latest
docker exec -it mongo bash

# inside the container:

# install wget
apt update
apt install wget

# download the json file
wget https://raw.githubusercontent.com/zrlu/mosaic-project/main/project.json

# load
mongoimport project.json
mongoimport --db test --collection project project.json
```

## Start the server

Install Python 3.9

```bash
# In your host machine:

pip install flask pymongo
python app.py
curl http://localhost:5000/search/project?projectSchoolName=I.S.%20254%20-%20BRONX
```
