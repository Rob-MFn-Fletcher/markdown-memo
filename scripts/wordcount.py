#!/usr/bin/env python
"""
NAME
    wordcount.py - short description

SYNOPSIS
    Put synposis here.

DESCRIPTION
    Put description here.

OPTIONS
    -h, --help
        Prints this manual and exits.
        
    -n VAL
        Blah blah.

AUTHOR
    Ryan Reece  <ryan.reece@cern.ch>

COPYRIGHT
    Copyright 2016 Ryan Reece
    License: GPL <http://www.gnu.org/licenses/gpl.html>

SEE ALSO
    ROOT <http://root.cern.ch>

TO DO
    - One.
    - Two.

2016-08-02
"""

#------------------------------------------------------------------------------
# imports
#------------------------------------------------------------------------------

## std
import argparse, sys, time
import pandas as pd
import matplotlib.pyplot as plt

# print(plt.style.available) # [u'dark_background', u'bmh', u'grayscale', u'ggplot', u'fivethirtyeight']
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15, 5)

## my modules

## local modules


#------------------------------------------------------------------------------
# globals
#------------------------------------------------------------------------------
timestamp = time.strftime('%Y-%m-%d-%Hh%M')
GeV = 1000.


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
            help='A positional argument.')
    parser.add_argument('-o', '--out',  default='wordcount', type=str,
            help="Some toggle option.")
    return parser.parse_args()


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    infile = ops.infile
    out = ops.out

    ## parse data
    df = pd.read_csv(infile, parse_dates=['Date'], index_col='Date')

    ## get the last day
    t2 = df.last_valid_index()
    d2 = t2.date()
    last_words = df['Words'][t2]
    last_pages = df['Pages'][t2]

    ## find data from the previous day
    prev_words = 0
    prev_pages = 0
    for t1 in reversed(df.index):
        d1 = t1.date()
        if d1 != d2:
            prev_words = df['Words'][t1]
            prev_pages = df['Pages'][t1]
            break

    ## make words plot
    ax = df['Words'].plot(marker='o',markersize=8)
#    ax.set_xlabel("Date")
    ax.set_xlabel("")
    ax.set_ylabel("Words")
    fig = ax.get_figure()
    fig.savefig('words.png')
    plt.close()

    print '%i words, %i written today' % (last_words, last_words-prev_words)

    ## make pages plot
    ax = df['Pages'].plot(marker='o',markersize=8)
#    ax.set_xlabel("Date")
    ax.set_xlabel("")
    ax.set_ylabel("Pages")
    fig = ax.get_figure()
    fig.savefig('pages.png')
    plt.close()

    print '%i pages, %i written today' % (last_pages, last_pages-prev_pages)


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def fatal(message=''):
    sys.exit("Fatal error in %s: %s" % (__file__, message))


#______________________________________________________________________________
def tprint(s, log=None):
    line = '[%s] %s' % (time.strftime('%Y-%m-%d:%H:%M:%S'), s)
    print line
    if log:
        log.write(line + '\n')
        log.flush()


#------------------------------------------------------------------------------
if __name__ == '__main__': main()

# EOF
