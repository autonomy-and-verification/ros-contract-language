#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.fol2latex import FOL2Latex
from translators.translator import Translator

""" Latex translator, which should output the contracts in Latex """

class Latex_Translator(Translator):

    def __init__(self, version, name):

        self.visitor = FOL2Latex()
        self.version = version
        self.name = name

    def translate(self, contract):

        contract.get_contract_name()

        output ="\\begin{description} \n"

        for n in contract.get_nodes():
            output += self._translate_node(n)

        output += "\n\\end{description}\n"
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

        return "\item[" + node_name + "] ~\\\\\n\\begin{itemize} \n" + topic_list_out + "\n" +  assumes_out + "\n" + guarantees_out + "\n\\end{itemize}\n"

    def _translate_topic_list(self, topic_list):
        assert(isinstance(topic_list, list))

        topics_out = "  \\item "
        if topic_list != []:
            topics_out += "topics ($"

            head, *tail = topic_list

            topics_out += self._translate_topic(head)

            if tail != None:
                if(isinstance(tail,list)):
                    for topic in tail:
                        topics_out += ", " + self._translate_topic(topic)
                else:
                    topics_out += ", " + self._translate_topic(tail)


            topics_out += "$)"

            return topics_out
        else:
            return topics_out + "topics ()"

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type, topic_name = topic.split(" ")

        return type.replace('_', '\_') +" "+ topic_name.replace('_', '\_')

    def _translate_assumes(self, short_name, assumes):
        assert(isinstance(assumes, list))

        ass_out = ""

        for ass in assumes:

            result = self.visitor.visit(ass)
            ass_out += "  \\item $\\mathcal{A}_" + short_name + "(\\overline{i_"+short_name+"}): " + result + "$\n"

        return ass_out

    def _translate_guarantees(self, short_name, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""

        for guar in guarantees:

            result = self.visitor.visit(guar)
            guar_out += "  \\item $\\mathcal{G}_" + short_name + "(\overline{o_" + short_name + "}): " + result + "$\n"
        return guar_out
