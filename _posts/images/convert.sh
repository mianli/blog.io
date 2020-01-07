#! /bin/bash
# export DYLD_LIBRARY_PATH="$HOME/ImageMagick-7.0.8/lib/"
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib/"
echo convert $1 -resize $2 $3
/Users/limian/ImageMagick-7.0.8/bin/convert $1 -resize $2 $3