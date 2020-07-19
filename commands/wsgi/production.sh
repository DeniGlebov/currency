#!/bin/bash

uwsgi --chdir /srv/project/src --http :8000 --module settings.wsgi --master --processes 4 --threads 2