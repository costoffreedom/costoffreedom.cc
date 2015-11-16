#!/usr/bin/bash

import os
import argparse
import markdown2
import sys

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

def main():

    # parse cli args
    parser  = argparse.ArgumentParser()
    parser.add_argument('file', default="file.md", help='Input a Markdown file')
    parser.add_argument( "-o" ,'--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')
    args = parser.parse_args()

    #load metata
    with open(args.file, "r") as f :
        raw = f.read()

        # parse metadata
        html = markdown2.markdown(raw, extras=["metadata"])

        # strip meta data
        text = raw.split( '---' )[2].split('<p class="author bio">')[0].decode("utf-8")

        # get bio // TODO : get bio from authors folder
        bio = raw.split('<p class="author bio">')[1].replace('{{ page.author }}', html.metadata["author"])

        # add h1 title
        final = """# %s
        %s
        > %s
        """%(html.metadata["title"].decode("utf-8"), text, bio)

        if args.outfile is sys.stdout : 
            sys.stdout.write( final.encode("utf-8") ) 
        else :
            with open(args.outfile, 'w') as f:
                f.write(final )



if __name__ == '__main__':
    main()
