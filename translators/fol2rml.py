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
        print("+++ eq_right")
        print(tree.children[1])
        print("+++")
        eq_right = self.visit(tree.children[1])
        print(eq_right)
        self.count = self.count + 1
        # if guarantee.children[0].data == "string_literal" and isinstance(guarantee.children[1], lexer.Token):
        if eq_right != 'TRUE':
            if self.variables:
                self.rml["event_types"].append("ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " matches { " + eq_left + " : " + eq_right + " };")
                self.rml["event_types"].append("not_ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " not matches ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + ";")
                return "ET" + str(self.count) + "(" + ','.join(self.variables) + ")"
            else:
                self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
                self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
                return "ET" + str(self.count)
        else:
            if eq_left.startswith('{'):
                eq_left = eq_left[1:len(eq_left)-1]
            if self.variables:
                self.rml["event_types"].append("ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " matches { " + eq_left + " };")
                self.rml["event_types"].append("not_ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " not matches ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + ";")
                return "ET" + str(self.count) + "(" + ','.join(self.variables) + ")"
            else:
                self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " };")
                self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
                return "ET" + str(self.count)
        # if eq_right in self.variables:
        #     self.rml["event_types"].append("ET" + str(self.count) + "(" + eq_right + ")" + " matches { " + eq_left + " : " + eq_right + " };")
        #     self.rml["event_types"].append("not_ET" + str(self.count) + "(" + eq_right + ")" + " not matches ET" + str(self.count) + "(" + eq_right + ")" + ";")
        #     return "ET" + str(self.count) + "(" + eq_right + ")"
        # else:
        #     self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
        #     self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
        #     return "ET" + str(self.count)

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")
        eq_left = self.visit(tree.children[0])
        eq_right = self.visit(tree.children[1])
        self.count = self.count + 1
        if self.variables:
            self.rml["event_types"].append("ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + " not matches ET" + str(self.count) + "(" + ','.join(self.variables) + ")" + ";")
            return "not_ET" + str(self.count) + "(" + ','.join(self.variables) + ")"
        else:
            self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
            self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
            return "not_ET" + str(self.count)
        # if eq_right in self.variables:
        #     self.rml["event_types"].append("ET" + str(self.count) + "(" + eq_right + ")" + " matches { " + eq_left + " : " + eq_right + " };")
        #     self.rml["event_types"].append("not_ET" + str(self.count) + "(" + eq_right + ")" + " not matches ET" + str(self.count) + "(" + eq_right + ")" + ";")
        #     return "not_ET" + str(self.count) + "(" + eq_right + ")"
        # else:
        #     self.rml["event_types"].append("ET" + str(self.count) + " matches { " + eq_left + " : " + eq_right + " };")
        #     self.rml["event_types"].append("not_ET" + str(self.count) + " not matches ET" + str(self.count) + ";")
        #     return "not_ET" + str(self.count)

    def atom(self, tree):
        """ Translate an atom tree """
        assert(tree.data == "atom")
        print("+++")
        print(tree)#
        print("+++")
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
            #print(v)
            #print(type(v))
            vars = self.visit(v)
            #print("!!")
            #print(vars)
        #    assert(False)
            self.variables.add(str(vars))
            if first:
                first = False
            else:
                vstr += ","
            vstr += str(vars)
        event_type = self.visit(tree.children[1])
        for v in tree.children[0].children:
            vars = self.visit(v)
            self.variables.remove(str(vars))
        return "{ let " + vstr + "; " + event_type + " }"

# MATT COPIED THIS IN AND EDITED IT
    def formula_variables_part(self, tree):
        """ Translate a formula_variables_part tree """
        assert(tree.data == "formula_variables_part")
        assert(len(tree.children) == 2)

        vars_extract, sets_extract = tree.children

        vars_out = ""
        for var in vars_extract.children:
            vars_out += self.visit(var)

#        if isinstance(sets_extract, Token):
#            sets_out = self.make_string(sets_extract)
#        elif isinstance(sets_extract, Tree):
#            sets_out = self.visit(sets_extract)

        return vars_out #+ " \\in " + sets_out
###

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        vstr = ""
        first = True
        for v in tree.children[0].children:

            vars = self.visit(v)
            self.variables.add(str(vars))
            if first:
                first = False
            else:
                vstr += ","
            vstr += str(vars)
        event_type = self.visit(tree.children[1])
        for v in tree.children[0].children:
            vars = self.visit(v)
            self.variables.remove(str(vars))
        return "{ let " + vstr + "; (" + event_type + " Any*) \\/ (Any)" + ") }"

## MATT Copied this from above, but it might need a different translation
    def exists_unique(self, tree):
        """ Translate a exists_unique tree """
        assert(tree.data == "exists_unique")
        assert(len(tree.children) == 2)

        vstr = ""
        first = True
        for v in tree.children[0].children:

            vars = self.visit(v)
            self.variables.add(str(vars))
            if first:
                first = False
            else:
                vstr += ","
            vstr += str(vars)
        event_type = self.visit(tree.children[1])
        for v in tree.children[0].children:
            vars = self.visit(v)
            self.variables.remove(str(vars))
        return "{ let " + vstr + "; (" + event_type + " Any*) \\/ (Any)" + ") }"


## REMOVED BY MATT
#    def terms(self, tree):
#       """ Translate a terms tree """
#        assert(tree.data == "terms")
#        return self.visit(tree.children)

#    def term(self, tree):
#        """ Translate a term tree """
#        assert(tree.data == "term")
#        return self.visit(tree.children[0])

    def sub_formula(self, tree):
        """ Translate a function tree """
        assert(tree.data == "sub_formula")
        #print(tree.children[0])
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
            #Matt added this bit, please check
            elif term.data == "not_in":
                term.data = "in_form"


            return term


# MATT ADDED THESE
#They're mostly just copied from fol2latex so please check
    def function_application(self, tree):
        """ Translate a function_application tree """
        assert(tree.data == "function_application")
        assert(len(tree.children) == 2)
        res = '{'
        res = res + self.visit(tree.children[0]) + ' : ['
        first = True
        for arg in tree.children[1].children:
            # if arg.children[0][0].isalpha():
            #     self.vars.add(arg.children[0])
            if first:
                first = False
            else:
                res = res + ', '
            res = res + self.visit(arg)
        res = res + ']}'
        return res

    def in_form(self, tree):
        """ Translate an in tree """
        assert(tree.data == "in_form")

        in_left, in_right = self.binary_infix(tree)

        return in_left + " \\in " + in_right

    def not_in(self, tree):
        """ Translate a not in tree """
        assert(tree.data == "not_in")
        assert(len(tree.children) == 2)

        in_left, in_right = self.binary_infix(tree)

        return in_left + " \\notin " + in_right

    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")

        head, *tail = tree.children

        if isinstance(head, Tree):
            vars = self.make_string(self.visit(head))
        else:
            vars = self.make_string(head)

        for var in tail:
            if isinstance(head, Tree):
                vars += ", " + self.make_string(self.visit(var))
            else:
                vars += ", " + self.make_string(var)

        assert(isinstance(vars, str))
        return "\\{" + vars + "\\}"

    def leq(self, tree):
        """ Translate a leq tree """
        assert(tree.data == "leq")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " \\leq " + right

    def geq(self, tree):
        """ Translate a geq tree """
        assert(tree.data == "geq")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " \\geq " + right

    def lt(self, tree):
        """ Translate a lt tree """
        assert(tree.data == "lt")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " < " + right

    def gt(self, tree):
        """ Translate a gt tree """
        assert(tree.data == "gt")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " > " + right

    def empty_set(self, tree):
        """ Translates an empty_set tree """
        assert(tree.data == "empty_set")

        return "{}"

    def variable_reference(self, tree):
        """Translates a reference to a variable, which may have an
         'in.' or 'out.' decoration. """
        assert(tree.data == "variable_reference")



        numberOfChildren = len(tree.children)
        assert(numberOfChildren in {1, 2})

        if numberOfChildren == 1:
            return tree.children[0]
        else:

            decoration, name = tree.children
            ## MATT: Ignoring the decoration, not needed for RML?
        #    decoration_out = self.visit(decoration)

        #    print("decoration =" + decoration_out)
            #print("name =" + name)
            return self.make_string(name)
            # This seems to be escaped elsewhere.
