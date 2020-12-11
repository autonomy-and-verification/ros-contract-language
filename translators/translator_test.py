#!/usr/bin/python
# -*- coding: utf-8 -*-
from lark import *
from translators.translator import Translator

class Test_Translator(Translator):

    def __init__(self):
        pass

    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node[0], lexer.Token) )
        node_name = node[0]
        node_contracts = node[1:]

        return node_name + "{" + self._translate_contract_block(node_contracts) + "}"

    def _translate_contract_block(self, contract_list):

        contracts = ""
        for cb in contract_list:
            contracts += self._translate_contract(cb)

        return contracts

    def _translate_contract(self, contract):
        """ Translate one contract """
        assert(isinstance(contract, tree.Tree) )

        topic, type_str, guar = contract.children

        return ("{" + topic + ";" + type_str + ";" + guar + "}")


    def translate(self, parseTree):
        """Translates the parse tree into RML output for ROS Mon"""

        output =""

        for t in parseTree.children:
            if t.data == 'node_clause':
                output += self._translate_node(t.children)
            else:
                output += "Not a Node"

        return output
