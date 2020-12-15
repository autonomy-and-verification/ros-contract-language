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

        guar = self._translate_fol(guar)



        return ("{" + topic + ";" + type_str + ";" + guar + "}")

    def _translate_fol(self, fol_statement):
        """ Translate a fol guarantee statement """


        if isinstance(fol_statement, tree.Tree):

            statement = fol_statement.data



            if statement == "formula":
                return self._translate_fol(fol_statement.children)
            elif statement == "implies":
                return self._translate_fol(fol_statement.children[0]) + " -> " + self._translate_fol(fol_statement.children[1])
            elif statement == "equals":
                return self._translate_fol(fol_statement.children[0]) + " == " + self._translate_fol(fol_statement.children[1])
            elif statement == "negation":

                return "not " + self._translate_fol(fol_statement.children)
            elif statement == "atom":
                return self._translate_fol(fol_statement.children[0])
            elif statement == "term":
                return self._translate_fol(fol_statement.children[0])
            elif statement == "predicate":
                print("!Predicate")
                print(fol_statement)
                return self._translate_fol(fol_statement.children[0]) + "("+ self._translate_fol(fol_statement.children[1]) +")"
            elif statement == "terms":
                return self._translate_fol(fol_statement.children)
            elif statement == "term":
                return self._translate_fol(statement.children)


        elif isinstance(fol_statement, lexer.Token):
            print("!Token")
            print(fol_statement)

            return fol_statement
        elif isinstance(fol_statement, list):
            # Catches children being a list and iterates.
            # Useful for one-or-more occurances
            for element in fol_statement:
                return self._translate_fol(element)
        else:
            return str(fol_statement)


    def translate(self, parseTree):
        """Translates the parse tree into RML output for ROS Mon"""

        output =""

        for t in parseTree.children:
            if t.data == 'node_clause':
                output += self._translate_node(t.children)
            else:
                output += "Not a Node"

        return output
