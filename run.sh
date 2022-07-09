#!/bin/bash

gunicorn --bind 0.0.0.0:8081 project.wsgi