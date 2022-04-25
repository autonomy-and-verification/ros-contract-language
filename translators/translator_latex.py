#!/usr/bin/python
# -*- coding: utf-8 -*-

from contract_model import Contract
from contract_model import Node
from contract_model import Type
from translators.fol2latex import FOL2Latex
from translators.translator import Translator

""" Latex translator, which should output the contracts in Latex """


class Latex_Translator(Translator):

    def __init__(self, version, name):

        self.visitor = FOL2Latex()
        self.version = version
        self.name = name

    def translate(self, contract):
        """ Translates a contract, calling other helper methods """
        assert(isinstance(contract, Contract))

        contract.get_contract_name()

        output = "\\begin{description} \n"

        output += self._translate_types(contract.get_types())

        for n in contract.get_nodes():
            output += self._translate_node(n)

        output += "\n\\end{description}\n"
        return output

    def _translate_types(self, types_list):
        """ Translates the list of types declared in the contract """
        assert(isinstance(types_list, list))

        types_out = "\\item[Context]~\\\\\n\\begin{itemize} \n"

        if not types_list:
            types_out += "\t\t\\item No Types Declared \n"

        for t in types_list:
            types_out += "\t\t\\item $ " + self._translate_type(t) + " $\n"

        types_out += "\\end{itemize}\n"
        return types_out

    def _translate_type(self, type_declaration):
        """ Translates one type declaration """
        assert(isinstance(type_declaration, Type))

        type_definition_out = self.visitor.visit(
            type_declaration.get_type_definition())

        print(type_declaration)
        print(type_definition_out)


        return type_declaration.get_type_name() + " : " + type_definition_out

    def _translate_node(self, node):
        """Traslates one node """
        assert(isinstance(node, Node))

        node_name = node.get_node_name()
        short_name = node_name[0].upper()

        inputs = node.get_input_list()
        outputs = node.get_output_list()
        topic_list = node.get_topic_list()
        assumes = node.get_assumes()
        guarantees = node.get_guarantees()

        inputs_out = self._translate_io("inputs", inputs)
        outputs_out = self._translate_io("outputs", outputs)
        topic_list_out = self._translate_topic_list(topic_list)
        assumes_out = self._translate_assumes(short_name, assumes)
        guarantees_out = self._translate_guarantees(short_name, guarantees)

        return "\\item[" + node_name + "] ~\\\\\n\\begin{itemize} \n" +\
            inputs_out + "\n" +\
            outputs_out + "\n" +\
            topic_list_out + "\n" +\
            assumes_out + "\n" +\
            guarantees_out +\
            "\n\\end{itemize}\n"

    def _translate_io(self, list_name, io_list):
        assert(isinstance(io_list, list))

        io_out = " \t\\item "
        if io_list != []:
            io_out += list_name + " ($ "

            head, *tail = io_list

            io_out += self._translate_io_var(head)

            if tail is not None:
                for io_var in tail:
                    io_out += ", " + self._translate_io_var(io_var)

            io_out += "$ )"
            return io_out
        else:
            return io_out + list_name + " ()"

    def _translate_io_var(self, io_var):

        name, type = io_var
        return name.replace('_', '\\_') + " : " + type.replace('_', '\\_')

    def _translate_topic_list(self, topic_list):
        assert(isinstance(topic_list, list))

        topics_out = " \t \\item "
        if topic_list != []:
            topics_out += "topics ($ "

            head, *tail = topic_list

            topics_out += self._translate_topic(head)

            if tail is not None:
                if(isinstance(tail, list)):
                    for topic in tail:
                        topics_out += ", \\\\" + self._translate_topic(topic)
                else:
                    topics_out += ", \\\\" + self._translate_topic(tail)

            topics_out += " $ )"

            return topics_out
        else:
            return topics_out + "topics () "

    def _translate_topic(self, topic):
        """Translate one topic statement """
        assert(len(topic) in {2, 3})

        if len(topic) == 3:
            type_name, topic_name, matches = topic
            matches_out = ""

            if len(matches.children) == 2:
                pointer, match_name = matches.children
                pointer = pointer.children[0]

                matches_out = pointer + match_name

            else:
                matches_out = matches.children[0]

            return type_name.replace('_', '\\_') + "~" + \
                topic_name.replace('_', '\\_') + "~matches:~" + \
                matches_out.replace('_', '\\_')

        elif len(topic) == 2:
            type_name, topic_name = topic
            return type_name.replace('_', '\\_') + "~" +\
                topic_name.replace('_', '\\_')

    def _translate_assumes(self, short_name, assumes):
        assert(isinstance(assumes, list))

        ass_out = ""

        for ass in assumes:

            result = self.visitor.visit(ass)
            ass_out += "  \\item $ \\mathcal{A}_" + short_name + \
                "(\\overline{i_"+short_name+"}): " + result + " $\n"

        return ass_out

    def _translate_guarantees(self, short_name, guarantees):
        assert(isinstance(guarantees, list))

        guar_out = ""

        for guar in guarantees:

            result = self.visitor.visit(guar)
            guar_out += "  \\item $ \\mathcal{G}_" + short_name + \
                "(\\overline{o_" + short_name + "}): " + result + " $\n"
        return guar_out
