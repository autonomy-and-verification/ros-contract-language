#!/usr/bin/python
# -*- coding: utf-8 -*-

from lark import *
from translators.translator import Translator
import yaml

class ROSMon_Translator(Translator):
    """Translator from Lark Parse Trees to ROSMon config and monitor files """

    def __init__(self):
        self.rosmon_config = {"nodes":[], "monitors":[]}

        self.nodes = []
        self.monitors = []


    def _add_node(self, node_name):
        print("adding node name: " + str(node_name))

        self.nodes.append( {"node":{"name":str(node_name)}} )

    def _add_monitor(self, type, topic_name):
        print("adding monitor for " +str(type) + " " + str(topic_name))

        self.monitors.append( {"monitor":{"id":"monitor_"+str(topic_name), "log": "./"+str(topic_name)+"_log.txt", "silent": "False", "topics":[{"name": str(topic_name), "type": "std_msgs.msg."+str(type), "action":"log"}]     }   } )


    def _prep_config(self):

        self.rosmon_config.update({"nodes":self.nodes})
        self.rosmon_config.update({"monitors":self.monitors})


    def translate(self, parse_tree):
        """Translates the parse tree into RML output for ROS Mon"""

        for t in parse_tree.children:
            assert(t.data == 'node_clause')

            self._translate_node(t.children)

        self._prep_config()
        return yaml.dump(self.rosmon_config)


    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node[0], lexer.Token) )

        node_name = node[0]
        node_contracts = node[1:]

        self._add_node(node_name)

        self._translate_contract_block(node_contracts)


    def _translate_contract_block(self, contract_list):

        contracts = ""
        for cb in contract_list:
            self._translate_contract(cb)



    def _translate_contract(self, contract):
        """ Translate one contract """
        assert(isinstance(contract, tree.Tree) )

        topic, guar = contract.children

        topic = self._translate_topic(topic)

        guar = self._translate_fol(guar)

        #return ("{ " + topic + guar + " }")



    def _translate_topic(self, topic):
        """Translate one topic statement """

        assert len(topic.children)  == 2
        type, topic_name = topic.children

        self._add_monitor(type, topic_name)

        #return "topic " + type +" "+ topic_name + " "

    def _translate_fol(self, fol_statement):
        """Translate the fol guarantee """
        # This ends up as a visitor or a big state machine
        pass
