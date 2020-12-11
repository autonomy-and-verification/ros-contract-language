#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Superclass of the translators """

class Translator(object):
    """ Superclass for the translators. This will be extended by classes to translate to specific languages """

    def __init__(self):
        pass

    def translate(self, parseTree):
        """Translates the parse tree into the desired output"""
        pass

    def _translate_node(self, node):
        """Traslates one node """
        pass

    def _translate_contract_block(self, contract_list):
        pass

    def _translate_contract(self, contract):
        """ Translate one contract """
        pass
