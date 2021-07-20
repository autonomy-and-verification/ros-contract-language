#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.fol2latex import FOL2Latex
from translators.translator import Translator

""" Latex translator, which should output the contracts in Latex """

class Latex_Translator(Translator):

    def __init__(self):

        self.visitor = FOL2Latex()

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
        short_name = node_name[0].upper()

        topic_list = node.get_topic_list()
        assumes = node.get_assumes()
        guarantees = node.get_guarantees()

        topic_list_out = self._translate_topic_list(topic_list)
        assumes_out = self._translate_assumes(short_name, assumes)
        guarantees_out = self._translate_guarantees(short_name, guarantees)

        return "node " + node_name + "\n{\n" + topic_list_out + "\n" + assumes_out + "\n" + guarantees_out + "\n}"

    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        if topic_list != []:
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
        else:
            return "topics ()"

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type, topic_name = topic.split(" ")

        return type +" "+ topic_name

    def _translate_assumes(self, short_name, assumes):
        assert(isinstance(assumes, list))


        ass_out = ""
        #visitor = FOL2Text()


        for ass in assumes:

            result = self.visitor.visit(ass)
            print(result)
            ass_out += "\\mathcal{A}_" + short_name + "(\\overline{i_"+short_name+"}): " + result + "\n"

        return ass_out

    def _translate_guarantees(self, short_name, guarantees):
        assert(isinstance(guarantees, list))


        guar_out = ""
        #visitor = FOL2Text()

        for guar in guarantees:
            guar_out += "\\mathcal{G}_" + short_name + "(\overline{o_" + short_name + "}): " + self.visitor.visit(guar) + "\n"
        return guar_out
