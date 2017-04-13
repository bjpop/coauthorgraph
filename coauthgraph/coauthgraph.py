'''
Module      : Main 
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 2016 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX

The program reads one or more input FASTA files. For each file it computes a
variety of statistics, and then prints a summary of the statistics as output.
'''

from __future__ import print_function
from argparse import ArgumentParser
import sys
import pkg_resources
import logging
import bibtexparser
from collections import defaultdict



EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
DEFAULT_VERBOSE = False
PROGRAM_NAME = "coauthgraph"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    parser = ArgumentParser(description='Read Bibtex file and generate coauthorship graph')
    parser.add_argument('--version',
        action='version',
        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    parser.add_argument('bibtex',
        metavar='BIBTEX_FILE',
        type=str,
        help='Input Bibtex file')
    return parser.parse_args()



def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
            level=logging.DEBUG,
            filemode='w',
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: {0}'.format(' '.join(sys.argv)))


class Name(object):
    def __init__(self, string):
        fields = string.split(', ')
        if len(fields) > 1:
            self.last = fields[0].strip()
        else:
            self.last = string.strip()
        if len(fields) == 2:
            first_name = fields[1]
            initial = first_name[0]
            self.first = initial
        else:
            self.first = '' 

    def __str__(self):
        result = ''
        if self.first:
            return str(self.first) + ' ' + self.last
        else:
            return self.last 

    def __lt__(self, other):
        # we order on last name first
        return (self.last, self.first) < (other.last, other.first)

    def __hash__(self):
        return hash((self.first, self.last))

    def __eq__(self, other):
        return (self.first, self.last) == (other.first, other.last)


def process_bibtex(bibtex_filename):
    # set of (author, author) pairs
    # to normalise the pairs we sort the authors into dictionary order
    edges = set() 
    all_authors = set()
    with open(bibtex_filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        for entry in bib_database.entries:
            paper_authors = set()
            author_list = entry['author']
            author_list = author_list.replace('\n', ' ')
            authors_names = [Name(name.strip()) for name in author_list.split(' and ')]
            for name in authors_names:
                paper_authors.add(name)
                all_authors.add(name)
            paper_authors = list(paper_authors)
            for author1_index in range(len(paper_authors)):
                for author2_index in range(author1_index + 1, len(paper_authors)):
                    edge = tuple(sorted([paper_authors[author1_index], paper_authors[author2_index]]))
                    edges.add(edge)
    return all_authors, edges
    #for author1, author2 in edges:
    #    print("{} : {}".format(author1, author2))

def render_to_json(all_authors, edges):
    #for author in all_authors:
    #    print("{{ data: {{ id: '{}' }} }},".format(author))
    seen_authors = set()
    for author1, author2 in edges:
        if author1.last == 'Pope' or author2.last == 'Pope':
            if author1 not in seen_authors:
                print("{{ data: {{ id: '{}' }} }},".format(author1))
                seen_authors.add(author1)
            if author2 not in seen_authors:
                print("{{ data: {{ id: '{}' }} }},".format(author2))
                seen_authors.add(author2)

    id = 0
    for author1, author2 in edges:
        if author1.last == 'Pope' or author2.last == 'Pope':
            print("{{ data: {{ id: '{}', source: '{}', target: '{}' }}}},".format(id, author1, author2))
            id += 1


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    all_authors, edges = process_bibtex(options.bibtex)
    render_to_json(all_authors, edges)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
