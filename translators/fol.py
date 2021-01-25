#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Superclass of the FOL translators, using Lark Interpreters """

from lark.visitors import Interpreter

class FOL(Interpreter):

    def guarantee(self, tree):
        pass

    def implies(self, tree):
        pass

    def equals(self, tree):
        pass

    def negation(self, tree):
        pass

    def atom(self, term):
        pass

    def term(self, tree):
        pass

    def predicate(self, tree):
        pass

    def terms(self, tree):
        pass

    def string_literal(self, tree):
        pass
