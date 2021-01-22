#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *

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

        head, body = topic_list[0:]

        topics_out += self._translate_topic(head)

        if body != None:
            if(isinstance(body,list)):
                for topic in body:
                    topics_out += ", " + self._translate_topic(topic)
            else:
                topics_out += ", " + self._translate_topic(body)


        topics_out += ")"

        return topics_out

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type, topic_name = topic.split(" ")

        return type +" "+ topic_name

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""

        for guar in guarantees:
            guar_out += "G (" + guar + ")\n"

        return guar_out


    
