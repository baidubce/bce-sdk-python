#!/bin/bash

VERSION="0.8.29"
TARGET="bce-python-sdk-$VERSION"
mkdir $TARGET
cp -rf baidubce sample setup.py README.txt $TARGET
zip -r ${TARGET}.zip $TARGET -x "*.svn*"
cp ${TARGET}.zip output
