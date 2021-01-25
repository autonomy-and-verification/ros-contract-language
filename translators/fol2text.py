#!/usr/bin/python
# -*- coding: utf-8 -*-

from lark.visitors import Interpreter

class FOL2Text(FOL):

        def guarantee(self, tree):
            assert(tree.data == "guarantee")
            print("visitor: " + str(tree.data))
            return "test " + str(tree.data)

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
