#!/bin/bash

BOOK_HOME_DIR=$(pwd)
BOOK_DIR=${BOOK_HOME_DIR%%/}/_book
BUILD_DIR=${BOOK_HOME_DIR%%/}/build
TEX_DIR=${BOOK_HOME_DIR%%/}/tex

# printf $BOOK_HOME_DIR
# printf $BOOK_DIR

rm -rf $BUILD_DIR # delete existing build
mkdir -p $BUILD_DIR # make sure it exists

IGNORED_REPS="authors"

# loop in files

for chapters in $(find $BOOK_DIR -maxdepth 1 -type d ! -name $IGNORED_REPS ); do
    printf $chapters\\n
    tex_chapter=$BUILD_DIR/$(basename $chapters)
    mkdir -p $tex_chapter # create dir 
    for text in $(find $chapters -maxdepth 1  -name '*.md' ! -name 'index.md'); do
    tex_filename=$(basename ${text%.md}.tex)
    tex_filepath=$tex_chapter/$tex_filename
    printf \\t$text\\n 
    printf \\t$tex_filepath\\n
    
    # clean markdown and pipe into pandoc conversion
    python ${BOOK_HOME_DIR}/bin/clean_markdown.py $text | pandoc --from=markdown --output=$tex_filepath 
    done;
done;

chmod -R 755 $BUILD_DIR

# add files to build
find $TEX_DIR -name "*.tex" -exec ln -s {} "$BUILD_DIR" \;
find $TEX_DIR -name "*.cls" -exec ln -s {} "$BUILD_DIR" \;
ln -s "${TEX_DIR}/includes" "${BUILD_DIR}/includes";

# loop inside folders


