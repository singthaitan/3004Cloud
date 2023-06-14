#!/bin/sh
python -m services.hg_accsvc &
python -m flask run
