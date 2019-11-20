#!/bin/sh

# ./bootstrap (5.2)
rm -r ./lib ./include ./local ./bin
virtualenv --clear . -p python3
./bin/pip3 install -U pip
./bin/pip3 install -r requirements-${1-5.2}.txt
ln -s plone-${1-5.2}.x.cfg buildout.cfg
./bin/buildout
