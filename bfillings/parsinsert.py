#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013--, biocore development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
"""Application controller for ParsInsert

designed for ParsInsert v1.03 """

from StringIO import StringIO
from os.path import splitext, join, abspath

from burrito.parameters import ValuedParameter, FlagParameter, MixedParameter
from burrito.util import (CommandLineApplication, FilePath, system,
                            CommandLineAppResult, ResultPath, remove,
                            ApplicationError)

from cogent.core.tree import PhyloNode
from cogent.parse.tree import DndParser
from cogent.core.moltype import DNA, RNA, PROTEIN
from cogent.core.alignment import SequenceCollection, Alignment
from cogent.parse.phylip import get_align_for_phylip


class ParsInsert(CommandLineApplication):
    """ParsInsert application Controller"""

    _command = 'ParsInsert'
    _input_handler = '_input_as_multiline_string'
    _parameters = {
                    # read mask from this file
                    '-m':ValuedParameter('-',Name='m',Delimiter=' '),

                    # read core tree sequences from this file
                    '-s':ValuedParameter('-',Name='s',Delimiter=' '),

                    # read core tree from this file
                    '-t':ValuedParameter('-',Name='t',Delimiter=' '),

                    # read core tree taxomony from this file
                    '-x':ValuedParameter('-',Name='x',Delimiter=' '),

                    # output taxonomy for each insert sequence to this file
                    '-o':ValuedParameter('-',Name='o',Delimiter=' '),

                    # create log file
                    '-l':ValuedParameter('-',Name='l',Delimiter=' '),

                    # number of best matches to display
                    '-n':ValuedParameter('-',Name='n',Delimiter=' '),

                    #percent threshold cutoff
                    '-c':ValuedParameter('-',Name='c',Delimiter=' '),
                   }

    def _handle_app_result_build_failure(self,out,err,exit_status,result_paths):
        """ Catch the error when files are not produced """
        raise ApplicationError, \
         'ParsInsert failed to produce an output file due to the following error: \n\n%s ' \
         % err.read()

    def _get_result_paths(self,data):
        """ Get the resulting tree"""
        result = {}
        result['Tree'] = ResultPath(Path=splitext(self._input_filename)[0] + \
                                                  '.tree')
        return result

def insert_sequences_into_tree(aln, moltype, params={}):
    """Returns a tree from placement of sequences
    """
    # convert aln to phy since seq_names need fixed to run through parsinsert
    new_aln=get_align_for_phylip(StringIO(aln))

    # convert aln to fasta in case it is not already a fasta file
    aln2 = Alignment(new_aln)
    seqs = aln2.toFasta()

    parsinsert_app = ParsInsert(params=params)
    result = parsinsert_app(seqs)

    # parse tree
    tree = DndParser(result['Tree'].read(), constructor=PhyloNode)

    # cleanup files
    result.cleanUp()

    return tree
