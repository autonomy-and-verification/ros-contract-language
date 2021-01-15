#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import Node
from contract_model import Contract
from lark import *

class Extractor(object):

    def __init__(self,  contract_name):
        self.extracted_contract = Contract(contract_name)

    def extract(self, parse_tree):
        """"Translates the parse tree into RML output for ROS Mon"""

        for t in parse_tree.children:
            assert(t.data == 'node_clause')
            self._translate_node(t.children)

        return self.extracted_contract

    def _translate_node(self, node):
        """Traslates one node """

        assert(isinstance(node[0], lexer.Token) )
        node_name = node[0]
        topic_list = node[1].children
        guarantees = node[2:]

        topic_list_out = self._translate_topic_list(topic_list)
        guarantees_out = self._translate_guarantees(guarantees)

        self.extracted_contract.add_node(node_name, topic_list_out, guarantees_out)


        #return "node " + node_name + "\n{\n" + topic_list_out + "\n" + guarantees_out + "\n}"

    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        topics_out = []

        head, body = topic_list[0:]

        topics_out.append(self._translate_topic(head))

        if body != None:
            if(isinstance(body,list)):
                for topic in body:
                    topics_out.append(self._translate_topic(topic))
            elif(isinstance(body, lark.Tree)):
                topics_out.append(self._translate_topic(body))


        return topics_out

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = []

        for guar in guarantees:
            guar_out.append(self._translate_fol(guar))

        return guar_out

    def _translate_topic(self, topic):
        assert len(topic.children)  == 2
        type, topic_name = topic.children

        return type +" "+ topic_name


    def _translate_fol(self, fol_statement):
        """ Translate a fol guarantee statement """

        if isinstance(fol_statement, tree.Tree):

            statement = fol_statement.data

            if statement == "guarantee":
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

                return self._translate_fol(fol_statement.children[0]) + "("+ self._translate_fol(fol_statement.children[1]) +")"
            elif statement == "terms":
                return self._translate_fol(fol_statement.children)
            elif statement == "term":
                return self._translate_fol(statement.children)


        elif isinstance(fol_statement, lexer.Token):

            return fol_statement
        elif isinstance(fol_statement, list):
            # Catches children being a list and iterates.
            # Useful for one-or-more occurances
            for element in fol_statement:
                return self._translate_fol(element)
        else:
            return str(fol_statement)



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
