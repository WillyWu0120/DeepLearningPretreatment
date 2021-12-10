#!/bin/sh

FILE=$1
echo $FILE
OUTPUT=${FILE%.pdf}

echo $OUTPUT
pdftoppm "$FILE" "$OUTPUT" -png