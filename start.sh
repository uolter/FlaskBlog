#!/bin/bash

if [ -f ./env.sh ]
then
  echo "Setting env parameters"
  source ./env.sh
fi

python manage.py runserver
