#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Translates FOL to RML, using a Lark Interpreter """

from translators.fol import FOL
from lark import *

class FOL2RML(FOL):

    def __init__(self):
        super(FOL, self).__init__()
        self.rml = {"event_types":[], "terms": []}
        self.count = 0
        self.variables = set()

    def get_rml(self):
        return self.rml

    def guarantee(self, tree):
        """ Translate a guarantee tree """
        assert(tree.data == "guarantee")
        self.rml["terms"].append(self.visit(tree.children[0]))
        self.rml["event_types"].append("Any matches {};")
        return

    def implies(self, tree):
        """ Translate an implies tree """
        assert(tree.data == "implies")
        event_type1 = self.visit(self.neg(tree.children[0]))
        event_type2 = self.visit(tree.children[1])
        return "(" + event_type1 + " \\/ " + event_type2 + ")"

    def equals(self, tree):
        """ Translate an equals tree """
        assert(tree.data == "equals")
        eq_left = self.visit(tree.children[0])
        eq_right = self.visit(tree.children[1])
        self.count = self.count + 1
        # if guarantee.children[0].data == "string_literal" and isinstance(guarantee.children[1], lexer.Token):
        if eq_right in self.variables:
            self.rml["event_types"].append("ET" + str(self.count) + "(" + eq_right + ")" + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + "(" + eq_right + ")" + " not matches ET" + str(self.count) + "(" + eq_right + ")" + ";")
            return "ET" + str(self.count) + "(" + eq_right + ")"
        else:
            self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
            return "ET" + str(self.count)

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")
        eq_left = self.visit(tree.children[0])
        eq_right = self.visit(tree.children[1])
        self.count = self.count + 1
        if eq_right in self.variables:
            self.rml["event_types"].append("ET" + str(self.count) + "(" + eq_right + ")" + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + "(" + eq_right + ")" + " not matches ET" + str(self.count) + "(" + eq_right + ")" + ";")
            return "not_ET" + str(self.count) + "(" + eq_right + ")"
        else:
            self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
            return "not_ET" + str(self.count)

    def atom(self, tree):
        """ Translate an atom tree """
        assert(tree.data == "atom")
        return self.visit(tree.children[0])

    def negation(self, tree):
        """ Translate a negation tree """
        assert(tree.data == "negation")
        return self.visit(self.neg(tree.children[0]))
        # return "not_" + self.visit(tree.children)

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and_form")
        event_type1 = self.visit(tree.children[0])
        event_type2 = self.visit(tree.children[1])
        return "(" + event_type1 + " /\\ " + event_type2 + ")"

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or_form")
        event_type1 = self.visit(tree.children[0])
        event_type2 = self.visit(tree.children[1])
        return "(" + event_type1 + " \\/ " + event_type2 + ")"

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        event_type1 = self.visit(tree.children[0])
        event_type2 = self.visit(tree.children[1])
        return "((" + event_type1 + " /\\ " + event_type2 + ") \\/ (" + "not_" + event_type1 + " /\\ " + "not_" + event_type2 + "))"

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        vstr = ""
        first = True
        for v in tree.children[0].children:
            self.variables.add(str(v))
            if first:
                first = False
            else:
                vstr += ","
            vstr += str(v)
        event_type = self.visit(tree.children[1])
        for v in tree.children[0].children:
            self.variables.remove(str(v))
        return "{ let " + vstr + "; " + event_type + " }"

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        vstr = ""
        first = True
        for v in tree.children[0].children:
            self.variables.add(str(v))
            if first:
                first = False
            else:
                vstr += ","
            vstr += str(v)
        event_type = self.visit(tree.children[1])
        for v in tree.children[0].children:
            self.variables.remove(str(v))
        return "{ let " + vstr + "; (" + event_type + " Any*) \\/ (Any)" + ") }"

    def terms(self, tree):
        """ Translate a terms tree """
        assert(tree.data == "terms")
        return self.visit(tree.children)

    def term(self, tree):
        """ Translate a term tree """
        assert(tree.data == "term")
        return tree.children[0]

    def predicate(self, tree):
        """ Translate a predicate tree """
        assert(tree.data == "predicate")
        pass

    def function(self, tree):
        """ Translate a function tree """
        assert(tree.data == "function")
        pass

    def sub_formula(self, tree):
        """ Translate a function tree """
        assert(tree.data == "sub_formula")
        print(tree.children[0])
        return self.visit(tree.children[0])

    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")
        return "'" + tree.children[0] + "'"

    def neg(self, term):
        if isinstance(term, lexer.Token):
            return term
        else:
            if term.data == "implies":
                term.data = "and_form"
                term.children[1] = self.neg(term.children[1])
            elif term.data == "iff":
                term.data = "and_form"
                left = Tree("or_form", [self.neg(term.children[0]),self.neg(term.children[1])])
                right = Tree("or_form", [term.children[0],term.children[1]])
                term.children[0] = left
                term.children[1] = right
            elif term.data == "and_form":
                term.data = "or_form"
                term.children[0] = self.neg(term.children[0])
                term.children[1] = self.neg(term.children[1])
            elif term.data == "or_form":
                term.data = "and_form"
                term.children[0] = self.neg(term.children[0])
                term.children[1] = self.neg(term.children[1])
            elif term.data == "forall":
                term.data = "exists"
                term.children[1] = self.neg(term.children[1])
            elif term.data == "exists":
                term.data = "forall"
                term.children[1] = self.neg(term.children[1])
            elif term.data == "equals":
                term.data = "not_equals"
            elif term.data == "not_equals":
                term.data = "equals"
            elif term.data == "sub_formula":
                term.children[0] = self.neg(term.children[0])
            elif term.data == "negation":
                term.data = term.children[0].data
                term.children[0] = term.children[0]
            elif term.data == "atom":
                term.children[0] = self.neg(term.children[0])

            return term
