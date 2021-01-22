#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import Node
from contract_model import Contract
from lark import *

class Extractor(object):

    def __init__(self,  contract_name):
        self.extracted_contract = Contract(contract_name)

    def extract(self, parse_tree):
        """"s the parse tree into RML output for ROS Mon"""

        for t in parse_tree.children:
            assert(t.data == 'node_clause')
            self.__node(t.children)

        return self.extracted_contract

    def __node(self, node):
        """Traslates one node """

        assert(isinstance(node[0], lexer.Token) )
        node_name = node[0]
        topic_list = node[1].children
        guarantees = node[2:]

        topic_list_out = self._extract_topic_list(topic_list)
        guarantees_out = self._extract_guarantees(guarantees)

        self.extracted_contract.add_node(node_name, topic_list_out, guarantees_out)


        #return "node " + node_name + "\n{\n" + topic_list_out + "\n" + guarantees_out + "\n}"

    def _extract_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        topics_out = []

        #Fancy Python 3 syntax for this split
        head, *tail = topic_list

        topics_out.append(self._extract_topic(head))

        if tail != None:
            if(isinstance(tail,list)):
                for topic in tail:
                    topics_out.append(self._extract_topic(topic))
            elif(isinstance(tail, lark.Tree)):
                topics_out.append(self._extract_topic(tail))


        return topics_out

    def _extract_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = []

        for guar in guarantees:
            #Simply appends the guarentee parse tree
            guar_out.append(guar)

        return guar_out

    def _extract_topic(self, topic):
        assert len(topic.children)  == 2
        type, topic_name = topic.children

        return type +" "+ topic_name


    def __str__(self):
        return self.extract()


if __name__ == "__main__":
    from lark import Lark
    test_name = "test_contract"

    parser = Lark(open("grammars/rcl.lark").read())

    parse_tree = parser.parse(open("test/test_contract.rcl").read())

    test_extractor = Extractor(test_name)
    contract = test_extractor.extract(parse_tree)
    print()
    print("test_extractor.extract()")
    print(str(contract))
    assert(contract.get_contract_name() == test_name)


    print()
