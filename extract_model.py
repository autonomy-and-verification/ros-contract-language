#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import Contract
from lark.lexer import Token
from lark import Tree


class Extractor(object):

    def __init__(self,  contract_name):
        self.extracted_contract = Contract(contract_name)

    def extract(self, parse_tree):
        """"parses the parse tree into RML output for ROS Mon"""

        for t in parse_tree.children:

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

    def __node(self, node_clause):
        """Traslates one node clause """

        assert(isinstance(node_clause, list))
        assert(isinstance(node_clause[0], Token))
        assert(node_clause[0].type == "NODE_NAME")

        node_name = node_clause[0]

        assert(isinstance(node_clause[1], Tree))
        assert(node_clause[1].data == "inputs")
        input_list = node_clause[1].children

        assert(isinstance(node_clause[2], Tree))
        assert(node_clause[2].data == "outputs")
        output_list = node_clause[2].children

        assert(isinstance(node_clause[3], Tree))
        assert(node_clause[3].data == "topic_list")
        topic_list = node_clause[3].children

        assumes, guarantees = self._extract_assumes_and_gurantees(node_clause[4:])

        input_list_out = self._extract_io(input_list)
        output_list_out = self._extract_io(output_list)
        topic_list_out = self._extract_topic_list(topic_list)
        assumes_out = self._extract_assumes(assumes)
        guarantees_out = self._extract_guarantees(guarantees)

        self.extracted_contract.add_node(
            node_name, input_list_out, output_list_out, topic_list_out, assumes_out, guarantees_out)

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

    def _extract_io(self, io_list):
        assert(isinstance(io_list, list))

        if io_list != []:
            io_out = []
            head, *tail = io_list

            io_out.append(self._extract_io_var(head.children[0]))

            if tail is not None:
                for io in tail:
                    io_out.append(self._extract_io_var(io.children[0]))

            return io_out
        else:
            return []

    def _extract_io_var(self, io_var):
        assert(isinstance(io_var, Tree))

        print(io_var)
        name, type = io_var.children

        return (name, type)

    def _extract_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        if topic_list != []:
            topics_out = []

            # Fancy Python 3 syntax for this split
            head, *tail = topic_list

            topics_out.append(self._extract_topic(head))

            if tail is not None:
                if(isinstance(tail, list)):
                    for topic in tail:
                        topics_out.append(self._extract_topic(topic))
                elif(isinstance(tail, Tree)):
                    topics_out.append(self._extract_topic(tail))

            return topics_out
        else:
            return []

    def _extract_assumes(self, assumes):
        assert(isinstance(assumes, list))

        ass_out = []

        for ass in assumes:
            # Simply appends the assume parse tree
            ass_out.append(ass)

        return ass_out

    def _extract_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = []

        for guar in guarantees:
            # Simply appends the guarentee parse tree
            guar_out.append(guar)

        return guar_out

    def _extract_topic(self, topic):
        assert(isinstance(topic, Tree))
        assert(len(topic.children) in {2, 3})

        if len(topic.children) == 3:
            type, topic_name, matches = topic.children
            return (type, topic_name, matches)
        else:
            type, topic_name = topic.children
            return (type, topic_name)

    def __str__(self):
        return self.extract()


if __name__ == "__main__":
    from lark import Lark
    test_name = "navigation"

    parser = Lark(open("grammars/rcl.lark").read())

    parse_tree = parser.parse(open("test/test_contract.rcl").read())

    test_extractor = Extractor(test_name)
    contract = test_extractor.extract(parse_tree)
    print()
    print("test_extractor.extract()")
    print(str(contract))
    assert(contract.get_contract_name() == test_name)

    print()
