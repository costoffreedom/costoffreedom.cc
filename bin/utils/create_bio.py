#!/usr/bin/bash

import os
import argparse
import markdown2
import sys
import html2text
from slugify import slugify
import codecs

BOOK_DIR = os.path.join(os.getcwd(), "book")
AUTHORS_DIR = os.path.join(BOOK_DIR,"authors")

print "Parsing book at %s "%BOOK_DIR

chapters = ["affordances" , "architectonics-of-power" , "collective-memory" , "epilogue" , "opening:freedom" , ]

def create_bio(text_path):

    available_authors = [author for author in os.listdir(AUTHORS_DIR)]

    print "...  %s "%text_path

    #load metata
    with open(text_path, "r") as f :
        raw = f.read()

        # parse metadata
        html = markdown2.markdown(raw, extras=["metadata"])
        # print html.metadata

        author_slug = slugify(html.metadata["author"])
        outfile = "%s.md"%author_slug

        # check if already exists
        if outfile not in available_authors:

            # get bio // TODO : get bio from authors folder
            bio = raw.decode("utf-8").split('<p class="author bio">')[1].replace('{{ page.author }}', html.metadata["author"])

            # convert to markdown
            bio_md = html2text.html2text(bio)

            # get text URL
            relative_url = text_path.split("/")[-2:]
            text_url="/".join(relative_url)[:-3]
            print text_url

            # parse final bio
            final="""---
title: %s
section: Authors
layout: author
link: %s
---
%s
"""%(html.metadata["author"], text_url, bio_md)
            print final
            with codecs.open(os.path.join(AUTHORS_DIR, outfile), 'w', "utf-8") as f:
                f.write(final)
            print "%s : saved"%outfile
        else :
            print "%s : already exists"%outfile



def main():
    for chapter in chapters:
        chapter_path= os.path.join(BOOK_DIR,chapter)
        for text in  os.listdir(chapter_path):
            print text
            if text != "index.md":
                text_path = os.path.join(chapter_path,text)
                create_bio(text_path)



if __name__ == '__main__':
    main()
