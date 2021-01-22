#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.translator import Translator
import yaml

class ROSMon_Translator(Translator):
    """Translator from Lark Parse Trees to ROSMon config and monitor files """

    def __init__(self, contract):
        self.contract = contract

        self.rosmon_config = {"nodes":[], "monitors":[]}

        self.nodes = []
        self.monitors = []

        self.run_translate = False


    def _add_node(self, node_name):
        #print("adding node name: " + str(node_name))

        self.nodes.append( {"node":{"name":str(node_name)}} )

    def _add_monitor(self, type, topic_name):
        #print("adding monitor for " +str(type) + " " + str(topic_name))

        self.monitors.append( {"monitor":{"id":"monitor_"+str(topic_name), "log": "./"+str(topic_name)+"_log.txt", "silent": False, "topics":[{"name": str(topic_name), "type": "std_msgs.msg."+str(type), "action":"log"}]     }   } )


    def _prep_config(self):

        self.rosmon_config.update({"nodes":self.nodes})
        self.rosmon_config.update({"monitors":self.monitors})

    def translate(self, contract):
        """Translates the parsed contract object into RML output for ROS Mon"""

        contract.get_contract_name()

        output =""

        for n in contract.get_nodes():
            output += self._translate_node(n)

        return output

    def translate_config(self):


        if self.run_translate:
            pass
        else:
            self.translate(self.contract)

        self._prep_config()
        return yaml.dump(self.rosmon_config)


    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node, Node))

        node_name = node.get_node_name()

        topic_list = node.get_topic_list()
        guarantees = node.get_guarantees()

        self._add_node(node_name)

        topic_list_out = self._translate_topic_list(topic_list)
        guarantees_out = self._translate_guarantees(guarantees)

        return "node " + node_name + "\n{\n" + topic_list_out + "\n" + guarantees_out + "\n}"


    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
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

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type, topic_name = topic.split(" ")

        self._add_monitor(type, topic_name)

        return type +" "+ topic_name

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""

        for guar in guarantees:
            guar_out += "G (" + guar + ")\n"

        return guar_out
