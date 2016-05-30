# coding: utf-8

# The role :hover:`word,term` provides an inline highlight of 'word' with a mouse-over 
# translation from Icelandic to English of 'term' according to the stae.is/os database.
# In the case of :hover:`word`. The string 'term' is assumed to be the same as 'word'

# Author: Símon Böðvarsson
# 30.05.2016

from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes

def hover_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # for text input of the form: "word,term"
    try:
        [word,term] = text.split(",")
    # If no term is provided, it is assumed to be the same as word.
    except ValueError: 
        word=term=text

    node = make_hover_node(word,term)
    return [node],[]

def make_hover_node(word,term):
    # Tooltip HTML code.
    code = '<a href="http://www.stae.is/fletta/'+term+'" class="tooltip" target="_blank">'+word+u'<span><strong>Smelltu</strong> fyrir stae.is grein um hugtakið: <i>'+term+'</i></span></a>'

    # Create new hover object.
    node = hover()
    # Add the relevant code to the object.
    node.code = code
    return node

class hover(nodes.General, nodes.Element):
    code = ''
    pass

def html_hover_visit(self,node):
    # If HTML is to be generated, append the code.
    self.body.append(node.code)

def html_hover_depart(self,node):
    pass

def tex_hover_visit(self,node):
    # If TEX code is to be generated, do nothing.
    pass

def tex_hover_depart(self,node):
    pass

def setup(app):
    # Extension setup.
    app.add_node(hover, html = (html_hover_visit, html_hover_depart), latex = (tex_hover_visit, tex_hover_depart))
    app.add_role('hover',hover_role)