#!/bin/sh

FILE=$1
echo $FILE
OUTPUT="${FILE%.png}-rotated.png"

echo $OUTPUT
convert -rotate 90 "$FILE" $OUTPUT