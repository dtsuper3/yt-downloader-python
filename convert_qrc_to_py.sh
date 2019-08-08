#!/bin/bash
pyrcc5 -o photo_rc.py photo.qrc
pyuic5 -x main.ui -o mainUI.py