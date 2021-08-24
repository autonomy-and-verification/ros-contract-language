#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node(object):

    def __init__(self, node_name, topic_list, assumes, guarantees):
        assert(isinstance(node_name, str))
        assert(isinstance(topic_list, list))
        assert(isinstance(assumes, list))
        assert(isinstance(guarantees, list))

        self.node_name = node_name
        self.topic_list = topic_list
        self.assumes = assumes
        self.guarantees = guarantees

    def get_node_name(self):
        return self.node_name

    def get_topic_list(self):
        return self.topic_list

    def get_assumes(self):
        return self.assumes

    def get_guarantees(self):
        return self.guarantees


class Type(object):

    def __init__(self, type_name, type_definition):
        assert(isinstance(type_name, str))
    #    assert(isinstance(type_definition, str))
        self.type_name = type_name
        self.type_definition = type_definition

    def get_type_name(self):

        return self.type_name

    def get_type_definition(self):

        return self.type_definition

    def __str__(self):

        return self.get_type_name() + " : " + str(self.get_type_definition())


class Contract(object):

    def __init__(self, contract_name):
        self.contract_name = contract_name
        self.nodes = []
        self.types = []

    def set_contract_name(self, name):
        assert(isinstance(name, str))
        self.contract_name = name

    def get_contract_name(self):
        return self.contract_name

    def get_nodes(self):
        return self.nodes

    def add_node(self, node_name, topic_list, assumes, guarantees):

        assert(isinstance(node_name, str))
        assert(isinstance(topic_list, list))
        assert(isinstance(assumes, list))
        assert(isinstance(guarantees, list))

        new_node = Node(node_name, topic_list, assumes, guarantees)

        self.nodes.append(new_node)

    def get_types(self):
        assert(isinstance(self.types, list))
        return self.types

    def add_type(self, type_name, type_definition):
        assert(isinstance(self.types, list))
        new_type = Type(type_name, type_definition)

        self.types.append(new_type)
        assert(isinstance(self.types, list))

    def __str__(self):
        to_string = "contract:" + self.get_contract_name() + "\n"

        type_list = self.get_types()

        to_string += "types: \n"
        if type_list is not None:
            if type_list == []:
                to_string += "\ttype list empty \n"
            else:
                for type in type_list:
                    to_string += "\t" + str(type) + "\n"

        node_list = self.get_nodes()

        if node_list is not None:
            if node_list == []:
                to_string += "node list empty \n"
            else:
                for node in node_list:
                    to_string += "node: " + node.get_node_name() + "\n" + "\ttopics: " + str(node.get_topic_list()) + \
                                                               "\n" + "\tassumes:" + \
                                                                   str(node.get_assumes(
                                                                   )) + "\n \tguarantees: " + str(node.get_guarantees())

        return to_string


if __name__ == "__main__":
    test_contract = Contract("Test")
    test_contract.set_contract_name("Test Contract")

    node_name = "Test Node"
    topic_list = [("bool", "test"), ("String", "data")]
    assumes = ["true"]
    guarantees = ["true", "false", "x == y"]

    test_contract.add_node(node_name, topic_list, assumes, guarantees)

    print(test_contract)
