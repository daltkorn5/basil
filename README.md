# basil
Simple Personal Finance Application

###
Right now this is just notes for testing/setup and such, eventually I'll clean it up
and make it a real README
###

Notes
* Uses python3.7 currently
* Uses docker (installed via https://docs.docker.com/docker-for-mac/install/)
* Upgraded macos to 10.12 (macOS Sierra)

Py Env Stuff
* pip3 install pipenv
* pipenv --three to create virtual environment
* pipenv install -r requirements.txt

To run:
* execute bootstrap.sh

To get into DB:
* psql -h localhost -d basil_dev -p 5432 -U basil -W

Docker command to create psql db:
docker run --name basil-db \
  -p 5433:5433 \
  -e POSTGRES_DB=basil \
  -e POSTGRES_PASSWORD=basil \
  -d postgres

----------
Test post commands:
curl -X POST -H 'Content-Type: application/json' \
  -d '{"transaction_date": "2019-05-05", "amount": "20.00", "category_id": 1, "description": "Test transaction", "created_by": "daltkorn"}' \
  http://0.0.0.0:5000/transaction/add

curl http://0.0.0.0:5000/transaction/get_all

curl http://0.0.0.0:5000/transaction/aggregate

curl -X POST -H 'Content-Type: application/json' \
  -d '{"name": "Another Category"}' http://0.0.0.0:5000/category/add

curl -X POST -H 'Content-Type: application/json' \
  -d '{"transaction_id": 59}' \
  http://0.0.0.0:5000/transaction/set_category/1
---------

Installed Postgres Locally:
https://www.postgresql.org/download/macosx/
Need to append "/Library/PostgreSQL/11/bin/" to PATH in order to make the psql command line tool available

ORM Decision
* Will start off using ORMs because this application will generally rely on simple queries

### HAVEN'T DONE ANY FRONTEND YET
Angular Env Stuff
* To get nvm (node version manager): curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
* nvm install node to install latest version of node.js
* To get angular CLI: npm install -g @angular/cli
