#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import *
from translators.translator import Translator
from translators.fol2rml import FOL2RML
import yaml

class ROSMon_Translator(Translator):
    """Translator from Lark Parse Trees to ROSMon config and monitor files """

    def __init__(self, contract):
        self.contract = contract

        self.rosmon_config = {"nodes":[], "monitors":[]}

        self.nodes = []
        self.monitors = []
        self.dict_names = {}

        self.run_translate = False
        self.rml = None


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
        rml = ""
        for et in self.rml["event_types"]:
            rml += et + "\n"
        first = True
        rml += "\nMain = "
        for t in self.rml["terms"]:
            if first:
                first = False
            else:
                rml += " /\\ "
            rml += "(" + t + "*)"
        rml += ";\n"
        for dn in self.dict_names:
            rml = rml.replace(dn, self.dict_names[dn])
        return yaml.dump(self.rosmon_config), rml


    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node, Node))

        node_name = node.get_node_name()

        topic_list = node.get_topic_list()
        guarantees = node.get_guarantees()

        self._add_node(node_name)

        topic_list_out = self._translate_topic_list(topic_list)
        self.rml = self._translate_guarantees(guarantees)
        rmlstr = str(self.rml)
        for dn in self.dict_names:
            rmlstr = rmlstr.replace(dn, self.dict_names[dn])
            topic_list_out = topic_list_out.replace(dn, self.dict_names[dn])

        return "node " + node_name + "\n{\n" + topic_list_out + "\n" + rmlstr + "\n}"


    def _translate_topic_list(self, topic_list):

        assert(isinstance(topic_list, list))
        if topic_list != []:
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
        else:
            return "topics ()"

    def _translate_topic(self, topic):
        """Translate one topic statement """

        type = str(topic[0])
        topic_name = str(topic[1])
        matches_name = str(topic[2].children[0])
        self.dict_names[matches_name] = topic_name

        self._add_monitor(type, topic_name)

        return type +" "+ topic_name

    def _translate_guarantees(self, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""
        #This is the visitor class
        visitor = FOL2RML()

        for guar in guarantees:
            visitor.visit(guar)

        return visitor.get_rml()
