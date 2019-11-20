#!/bin/sh

# ./bootstrap (5.1|5.2)
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install -U pip
./bin/pip install -r requirements-$1.txt
ln -s plone-$1.x.cfg buildout.cfg
./bin/buildout
