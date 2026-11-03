#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.fol2text import FOL2Text
from translators.translator import Translator

""" Mirror translator, which should output the input contract """


class Mirror(Translator):

    def __init__(self):
        self.fol_visitor = FOL2Text()
        

    def translate(self, contract):

        contract_name = contract.get_contract_name()

        output = "\nContract: " + contract_name + "\n"

        for n in contract.get_nodes():
            output += self._translate_node(n)

        return output

    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node, Node))

        node_name = node.get_node_name()

        topic_list = node.get_topic_list()
        assumes = node.get_assumes()
        guarantees = node.get_guarantees()

        topic_list_out = self._translate_topic_list(topic_list)
        assumes_out = self._translate_assumes(assumes)
        guarantees_out = self._translate_guarantees(guarantees)

        return "node " + node_name + "\n{\n" + topic_list_out + "\n\n" + assumes_out + "\n\n" + guarantees_out + "}"

    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        if topic_list != []:
            topics_out = "Topics ("

            head, *tail = topic_list

            topics_out += self._translate_topic(head)

            if tail != None:
                if(isinstance(tail, list)):
                    for topic in tail:
                        topics_out += ", " + self._translate_topic(topic)
                else:
                    topics_out += ", " + self._translate_topic(tail)

            topics_out += ")"

            return topics_out
        else:
            return "topics ()"

    def _translate_topic(self, topic):
        """Translate one topic statement """
        assert(len(topic) in {2, 3})

        
        if len(topic) == 3:
            topic_type, topic_name, matches = topic
            matches_out = ""

            if len(matches.children) == 2:
                pointer, match_name = matches.children
                pointer = pointer.children[0]

                matches_out = pointer + match_name

            else:
                matches_out = matches.children[0]

            return topic_type + " " + topic_name + " matches " + matches_out
        elif len(topic) == 2:
            topic_type, topic_name = topic
            return topic_type + " " + topic_name
        

    def _translate_assumes(self, assumes):
        assert(isinstance(assumes, list))

        ass_out = ""
    
        for ass in assumes:

            ass_out += "Assumes (" + self.fol_visitor.visit(ass) + ")\n"

        return ass_out

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""
    
        for guar in guarantees:

            guar_out += "Guarantees (" + self.fol_visitor.visit(guar) + ")\n"

        return guar_out

    # This has been replaced

    def _translate_fol(self, fol_statement):
        """ Translate a fol guarantee statement """

        assert(false)

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

                return self._translate_fol(fol_statement.children[0]) + "(" + self._translate_fol(fol_statement.children[1]) + ")"
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
