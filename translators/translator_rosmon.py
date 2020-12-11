#!/usr/bin/python
# -*- coding: utf-8 -*-

from lark import *
from translators.translator import Translator

class ROSMon_Translator(Translator):

    def __init__(self):
        pass

    def translate(self, parseTree):
        """Translates the parse tree into RML output for ROS Mon"""
        pass

    def _translate_node(self, node):
        """Traslates one node """
        pass

    def _translate_contract_block(self, contract_list):
        pass

    def _translate_contract(self, contract):
        """ Translate one contract """
        pass
