#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.fol2text import FOL2Text

""" Mirror translator, which should output the input contract """

class Mirror(object):

    def __init__(self):
        pass

    def translate(self, contract):

        contract.get_contract_name()

        output =""

        for n in contract.get_nodes():
            output += self._translate_node(n)

        return output

    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node, Node))

        node_name = node.get_node_name()

        topic_list = node.get_topic_list()
        guarantees = node.get_guarantees()


        topic_list_out = self._translate_topic_list(topic_list)
        guarantees_out = self._translate_guarantees(guarantees)

        return "node " + node_name + "\n{\n" + topic_list_out + "\n" + guarantees_out + "\n}"

    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        topics_out = "topics ("

        head, *tail = topic_list

        topics_out += self._translate_topic(head)

        if tail != None:
            if(isinstance(tail,list)):
                for topic in tail:
                    topics_out += ", " + self._translate_topic(topic)
            else:
                topics_out += ", " + self._translate_topic(tail)


        topics_out += ")"

        return topics_out

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type, topic_name = topic.split(" ")

        return type +" "+ topic_name

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""
        visitor = FOL2Text()

        for guar in guarantees:
            guar_out += "G (" + visitor.visit(guar) + ")\n"

        return guar_out










    # This has been replaced
    def _translate_fol(self, fol_statement):
        """ Translate a fol guarantee statement """

        if isinstance(fol_statement, tree.Tree):

            statement = fol_statement.data

            #Wont we always start here...?
            if statement == "guarantee":
                return self._translate_fol(fol_statement.children)
            elif statement == "implies":
                return self._translate_fol(fol_statement.children[0]) + " -> " + self._translate_fol(fol_statement.children[1])
            elif statement == "equals":
                eq_left = self._translate_fol(fol_statement.children[0])
                eq_right = self._translate_fol(fol_statement.children[1])

                eq_out = eq_left + " == " + eq_right

                return eq_out
            elif statement == "negation":

                return "not " + self._translate_fol(fol_statement.children)
            elif statement == "atom":
                return self._translate_fol(fol_statement.children[0])
            elif statement == "term":
                return self._translate_fol(fol_statement.children[0])
            elif statement == "predicate":

                return self._translate_fol(fol_statement.children[0]) + "("+ self._translate_fol(fol_statement.children[1]) +")"
            elif statement == "terms":
                return self._translate_fol(fol_statement.children)
            elif statement == "term":
                return self._translate_fol(statement.children)
            elif statement == "string_literal":
                return "\"" + fol_statement.children[0] + "\""
        elif isinstance(fol_statement, lexer.Token):

            return fol_statement
        elif isinstance(fol_statement, list):
            # Catches children being a list and iterates.
            # Useful for one-or-more occurances
            for element in fol_statement:
                return self._translate_fol(element)
        else:
            return str(fol_statement)
