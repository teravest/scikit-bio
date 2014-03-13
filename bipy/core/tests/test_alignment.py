#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013--, bipy development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from unittest import TestCase, main

from bipy.core.sequence import (BiologicalSequence, NucleotideSequence, 
        DNASequence, RNASequence)
from bipy.core.alignment import (SequenceCollection, Alignment)
from bipy.core.exception import SequenceCollectionError


class SequenceCollectionTests(TestCase):
    """ Tests of the SequenceCollection class """

    def setUp(self):
        """ Initialize values to be used in tests
        """
        self.d1 = DNASequence('GATTACA', identifier="d1")
        self.d2 = DNASequence('TTG', identifier="d2")
        self.r1 = RNASequence('GAUUACA', identifier="r1")
        self.r2 = RNASequence('UUG', identifier="r2")
        self.r3 = RNASequence('U-----UGCC--', identifier="r3")
        
        self.seqs1 = [self.d1, self.d2]
        self.seqs2 = [self.r1, self.r2, self.r3]
        self.seqs3 = self.seqs1 + self.seqs2

        self.seqs1_t = [('d1', 'GATTACA'), ('d2', 'TTG')]
        self.seqs2_t = [('r1', 'GAUUACA'), ('r2', 'UUG'),
                ('r3', 'U-----UGCC--')]
        self.seqs3_t = self.seqs1_t + self.seqs2_t

        self.s1 = SequenceCollection(self.seqs1_t, DNASequence)
        self.s2 = SequenceCollection(self.seqs2_t, RNASequence)
        self.s3 = SequenceCollection(self.seqs3_t, NucleotideSequence)

    def test_init(self):
        """ Initialization functions as expected with varied input types
        """
        SequenceCollection(self.seqs1_t, BiologicalSequence)
        SequenceCollection(self.seqs1_t, NucleotideSequence)
        SequenceCollection(self.seqs1_t, DNASequence)
        
        SequenceCollection(self.seqs2_t, BiologicalSequence)
        SequenceCollection(self.seqs2_t, NucleotideSequence)
        SequenceCollection(self.seqs2_t, RNASequence)
        
        SequenceCollection(self.seqs3_t, BiologicalSequence)
        SequenceCollection(self.seqs3_t, NucleotideSequence)

    def test_init_validate(self):
        """ initialization with validation functions as expected
        """
        SequenceCollection(self.seqs1_t, NucleotideSequence, validate=True)
        SequenceCollection(self.seqs1_t, DNASequence, validate=True)
        # can't validate self.seqs2_t as a DNASequences
        self.assertRaises(SequenceCollectionError, SequenceCollection,
                self.seqs2_t, DNASequence, validate=True)

    def test_count_center_spread(self):
        """ count_center_spread functions as expected
        """
        actual1 = self.s1.count_center_spread()
        self.assertEqual(actual1[0],2)
        self.assertAlmostEqual(actual1[1], 5.0, 3)
        self.assertAlmostEqual(actual1[2], 2.0, 3)

        actual2 = self.s2.count_center_spread()
        self.assertEqual(actual2[0],3)
        self.assertAlmostEqual(actual2[1], 7.333, 3)
        self.assertAlmostEqual(actual2[2], 3.682, 3)

        actual3 = self.s3.count_center_spread()
        self.assertEqual(actual3[0],5)
        self.assertAlmostEqual(actual3[1], 6.400, 3)
        self.assertAlmostEqual(actual3[2], 3.323, 3)

    def test_getitem(self):
        """ getitem functions as expected
        """
        self.assertEqual(self.s1[0], self.d1)
        self.assertEqual(self.s1[1], self.d2)
        self.assertEqual(self.s2[0], self.r1)
        self.assertEqual(self.s2[1], self.r2)
        
    def test_iter(self):
        """ iter functions as expected
        """
        s1_iter = iter(self.s1)
        count = 0
        for actual, expected in zip(s1_iter, self.seqs1):
            count += 1
            self.assertEqual(actual, expected)
        self.assertEqual(count, len(self.seqs1))
        self.assertRaises(StopIteration, s1_iter.next)

    def test_len(self):
        """ len functions as expected
        """
        self.assertEqual(len(self.s1),2)
        self.assertEqual(len(self.s2),3)
        self.assertEqual(len(self.s3),5)

    def test_is_valid(self):
        """ is_valid functions as expected
        """
        self.assertTrue(self.s1.is_valid())
        self.assertTrue(self.s2.is_valid())
        self.assertTrue(self.s3.is_valid())

        invalid_seqs1 = SequenceCollection(self.seqs2_t, DNASequence)
        self.assertFalse(invalid_seqs1.is_valid())
        invalid_seqs2 = SequenceCollection(self.seqs1_t, RNASequence)
        self.assertFalse(invalid_seqs2.is_valid())

    def test_sequence_lengths(self):
        """ sequence_lengths functions as expected
        """
        self.assertEqual(self.s1.sequence_lengths(), [7, 3])
        self.assertEqual(self.s2.sequence_lengths(), [7, 3, 12])
        self.assertEqual(self.s3.sequence_lengths(), [7, 3, 7, 3, 12])

    def test_to_fasta(self):
        """ to_fasta functions as expected
        """
        exp1 = ">d1\nGATTACA\n>d2\nTTG\n"
        self.assertEqual(self.s1.to_fasta(),exp1)
        exp2 = ">r1\nGATTACA\n>r2\nTTG\n>r3'U-----UGCC--\n"
        self.assertEqual(self.s1.to_fasta(),exp1)

if __name__ == "__main__":
    main()
