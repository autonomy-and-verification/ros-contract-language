#!/usr/bin/python
# -*- coding: utf-8 -*-

from lark.visitors import Interpreter
from lark.lexer import Token
from lark import Tree
from translators.fol import FOL

class FOL2Text(FOL):

        def assume(self, tree):
            """ Translate an assume tree """
            assert(tree.data == "assume")
            print("translating assume")
            print(tree.children[0])

            return self.visit(tree.children[0])

        def guarantee(self, tree):
            """ Translate a guarantee tree """
            assert(tree.data == "guarantee")

            print("translating guar")
            print(tree.children[0])

            return self.visit(tree.children[0])

        def implies(self, tree):
            """ Translate an implies tree """
            assert(tree.data == "implies")

            return self.visit(tree.children[0]) + " -> " + self.visit(tree.children[1])

        def atom(self, tree):
            """ Translate an atom tree """
            assert(tree.data == "atom")
            print("translating atom")
            print(tree.children[0])

            return self.visit(tree.children[0])

        def atomic_formula(self,tree):
            """ Translate an atomic_formula tree """
            assert(tree.data == "atomic_formula")
            print("translating atomic_formula")
            print(tree.children[0])

            if isinstance(tree.children[0], Token):
                token = tree.children[0]
                if token.type == "BOOLEAN":
                    return str(token)
            else:
                assert(isinstance(tree.children[0], Tree))
                return self.visit(tree.children[0])


        def equals(self, tree):
            """ Translate an equals tree """
            assert(tree.data == "equals")
            assert(len(tree.children)==2)

            eq_left = self.visit(tree.children[0])
            eq_right = self.visit(tree.children[1])

            return eq_left + " == " + eq_right

        def not_equals(self, tree):
            """ Translate a not equals tree """
            assert(tree.data == "not_equals")
            assert(len(tree.children)==2)

            eq_left = self.visit(tree.children[0])
            eq_right = self.visit(tree.children[1])

            return eq_left + " != " + eq_right

        def in_form(self, tree):
            """ Translate an in tree """
            assert(tree.data == "in_form")
            assert(len(tree.children)==2)

            print("translating an in")

            in_left = self.visit(tree.children[0])
            in_right =self.visit(tree.children[1])
            print("left = " + in_left)
            print("right = " + in_right)

            return in_left + " in " + in_right

        def negation(self, tree):
            """ Translate a negation tree """
            assert(tree.data == "negation")

            return "not " + self.visit(tree.children[0])

        def and_form(self, tree):
            """ Translate an and tree """
            assert(tree.data == "and")
            pass

        def or_form(self, tree):
            """ Translate a or tree """
            assert(tree.data == "or")
            pass

        def iff(self, tree):
            """ Translate a iff tree """
            assert(tree.data == "iff")
            pass

        def forall(self, tree):
            """ Translate a forall tree """
            assert(tree.data == "forall")
            pass

        def exists(self, tree):
            """ Translate a exists tree """
            assert(tree.data == "exists")
            pass

        def predicate(self, tree):
            """ Translate a predicate tree """
            assert(tree.data == "predicate")

            assert(isinstance(tree.children[0],Token ))
            pred_name = str(tree.children[0])
            pred_terms = self.visit(tree.children[1])

            return pred_name + "("+ str(pred_terms) +")"

        def terms(self, tree):
            """ Translate a terms tree """
            assert(tree.data == "terms")

            for c in tree.children:
                return self.visit(c)

        def term(self, tree):
            """ Translate a term tree """
            assert(tree.data == "term")
            print("translating term")
            print(tree.children[0])

            assert(len(tree.children)==1)
            assert(isinstance(tree.children[0],Token ))

            return str(tree.children[0])

        def set(self, tree):
            """Translates a set tree """
            assert(tree.data == "set")

            print("translating a set")

            head, *tail = tree.children

            vars = str(head)

            for var in tail:
                vars += ", " + str(var)

            return "{" + vars + "}"


        def function(self, tree):
            """ Translate a function tree """
            assert(tree.data == "function")

            assert(isinstance(tree.children[0],Token ))
            func_name = str(tree.children[0])
            func_args = self.visit(tree.children[1])

            return func_name + "("+ str(func_args) +")"

        def string_literal(self, tree):
            """ Translate a string literal tree """
            assert(tree.data == "string_literal")

            return "\"" + tree.children[0] + "\""
