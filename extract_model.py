#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import Node
from contract_model import Contract
from lark import *


class Extractor(object):

    def __init__(self,  contract_name):
        self.extracted_contract = Contract(contract_name)

    def extract(self, parse_tree):
        """"parses the parse tree into RML output for ROS Mon"""

        for t in parse_tree.children:
            print(t)
            assert(t.data == "contract_clause")
            assert(len(t.children) == 1)

            inner = t.children[0]
            if(inner.data == 'node_clause'):
                self.__node(inner.children)
            elif(inner.data == "type_clause"):
                self.__type_clause(inner.children)

        return self.extracted_contract

    def __type_clause(self, statements):
        """ Translates one type clause """

        for statement in statements:
            assert(len(statement.children) == 2)
            name = statement.children[0]
            type = statement.children[1]

            self.extracted_contract.add_type(name, type)

    def __node(self, node):
        """Traslates one node clause """

        assert(isinstance(node[0], lexer.Token))
        node_name = node[0]
        topic_list = node[1].children
        assumes, guarantees = self._extract_assumes_and_gurantees(node[2:])

        topic_list_out = self._extract_topic_list(topic_list)
        assumes_out = self._extract_assumes(assumes)
        guarantees_out = self._extract_guarantees(guarantees)

        self.extracted_contract.add_node(
            node_name, topic_list_out, assumes_out, guarantees_out)

    def _extract_assumes_and_gurantees(self, node_list):

        assumes = []
        guarantees = []

        for node in node_list:
            if node.data == "assume":
                assumes.append(node)
            elif node.data == "guarantee":
                guarantees.append(node)
            else:
                pass

        return assumes, guarantees

    def _extract_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        if topic_list != []:
            topics_out = []

            #Fancy Python 3 syntax for this split
            head, *tail = topic_list

            topics_out.append(self._extract_topic(head))

            if tail != None:
                if(isinstance(tail, list)):
                    for topic in tail:
                        topics_out.append(self._extract_topic(topic))
                elif(isinstance(tail, lark.Tree)):
                    topics_out.append(self._extract_topic(tail))

            return topics_out
        else:
            return []

    def _extract_assumes(self, assumes):
        assert(isinstance(assumes, list))

        ass_out = []

        for ass in assumes:
            #Simply appends the assume parse tree
            ass_out.append(ass)

        return ass_out

    def _extract_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = []

        for guar in guarantees:
            #Simply appends the guarentee parse tree
            guar_out.append(guar)

        return guar_out

    def _extract_topic(self, topic):
        assert len(topic.children) == 2
        type, topic_name = topic.children

        return type + " " + topic_name

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
