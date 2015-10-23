#!/usr/bin/env python2
# -*- coding: utf-8-*-
import unittest
import imp
from client import jasperpath
from .. import sphinxplugin


def cmuclmtk_installed():
    try:
        imp.find_module('cmuclmtk')
    except ImportError:
        return False
    else:
        return True


def pocketsphinx_installed():
    try:
        imp.find_module('pocketsphinx')
    except ImportError:
        return False
    else:
        return True


@unittest.skipUnless(cmuclmtk_installed(), "CMUCLMTK not present")
@unittest.skipUnless(pocketsphinx_installed(), "Pocketsphinx not present")
class TestSTT(unittest.TestCase):

    def setUp(self):
        self.jasper_clip = jasperpath.data('audio', 'jasper.wav')
        self.time_clip = jasperpath.data('audio', 'time.wav')

        self.passive_stt_engine = sphinxplugin.PocketsphinxSTTPlugin('unittest-passive', ['JASPER'])
        self.active_stt_engine = sphinxplugin.PocketSphinxSTTPlugin('unittest-active', ['TIME'])

    def testTranscribeJasper(self):
        """
        Does Jasper recognize his name (i.e., passive listen)?
        """
        with open(self.jasper_clip, mode="rb") as f:
            transcription = self.passive_stt_engine.transcribe(f)
        self.assertIn("JASPER", transcription)

    def testTranscribe(self):
        """
        Does Jasper recognize 'time' (i.e., active listen)?
        """
        with open(self.time_clip, mode="rb") as f:
            transcription = self.active_stt_engine.transcribe(f)
        self.assertIn("TIME", transcription)
