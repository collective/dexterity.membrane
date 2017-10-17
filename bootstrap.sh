#!/bin/sh

# ./bootstrap plone-*.cfg
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install -U pip
./bin/pip install -r requirements.txt
ln -s $1 buildout.cfg
./bin/buildout
