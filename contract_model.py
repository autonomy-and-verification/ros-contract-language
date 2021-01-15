#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node(object):

    def __init__(self, node_name, topic_list, guarantees):
        assert(isinstance(node_name,str))
        assert(isinstance(topic_list, list))
        assert(isinstance(guarantees, list))


        self.node_name  = node_name
        self.topic_list = topic_list
        self.guarantees = guarantees

    def get_node_name(self):
        return self.node_name

    def get_topic_list(self):
        return self.topic_list

    def get_guarantees(self):
        return self.guarantees


class Contract(object):

    def __init__(self, contract_name):
        self.contract_name = contract_name
        self.nodes = []

    def set_contract_name(self, name):
        assert(isinstance(name, str))
        self.contract_name = name

    def get_contract_name(self):
        return self.contract_name

    def get_nodes(self):
        return self.nodes

    def add_node(self, node_name, topic_list, guarantees):

        new_node = Node(node_name, topic_list, guarantees)

        self.nodes.append(new_node)

    def __str__(self):
        to_string = "contract:" + self.get_contract_name() +"\n"

        node_list = self.get_nodes()

        if node_list != None:
            if node_list == []:
                to_string += "node list empty"
            else:
                for node in node_list:
                    to_string += "node: " + node.get_node_name() +"\n" + "\ttopics: " + str(node.get_topic_list()) +"\n" + "\tguarantees: " + str(node.get_guarantees())

        return to_string



if __name__ == "__main__":
    test_contract = Contract()
    test_contract.set_contract_name("Test Contract")

    node_name = "Test Node"
    topic_list = ["bool test", "String data"]
    guarantees = ["true", "false", "x == y"]

    test_contract.add_node(node_name, topic_list, guarantees)

    print(test_contract)
