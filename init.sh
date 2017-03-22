#!/bin/bash

psql -U postgres <<EOSQL
  CREATE USER "dynforms" WITH PASSWORD 'dynforms';
  CREATE DATABASE "dynforms" OWNER "dynforms";
  GRANT ALL PRIVILEGES ON DATABASE dynforms TO dynforms;
EOSQL