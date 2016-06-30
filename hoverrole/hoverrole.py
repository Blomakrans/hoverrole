# -*- coding: UTF-8-sig -*-

# The role :hover:`word,term` provides an inline highlight of 'word' with a mouse-over 
# translation from Icelandic to English of 'term' according to the stae.is/os database.
# In the case of :hover:`word`. The string 'term' is assumed to be the same as 'word'

# Author: Símon Böðvarsson
# 29.06.2016

from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes
import ordaskra

def hover_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # for text input of the form: "word,term"
    try:
        [word,term] = text.split(",")
    # If no 'term' is provided, it is assumed to be the same as 'word'.
    except ValueError: 
        word=term=text

    node = make_hover_node(word,term)
    return [node],[]

def make_hover_node(word,term):
    # Get English translation of Icelandic term.
    translation = ordaskra.isTranslate(term)
    # If no translation is found, append error message instead of translation.
    if translation == '':
        errorMsg = u'Ekki fannst þýðing á hugtakinu: ' 
        codebit = '<a class="tooltip" target="_blank">'+word+'<span><staelink style="line-height:4px; font-size:80%;">'+errorMsg+'<i>'+term+'</i></staelink></span></a>'
    else:
        codebit = '<a href="http://www.stae.is/os/leita/'+unicode(translation.replace(" ","_"))+'" class="tooltip" target="_blank">'+word+'<span>en: <i>'+unicode(translation)+u'</i><staelink style="font-size:80%;"><br><strong>Smelltu</strong> fyrir ítarlegri þýðingu.</staelink></span></a>'

    # Create new hover object.
    node = hover()
    # Add the relevant codebit to the object.
    node['code'] = codebit
    node['word'] = word
    return node

class hover(nodes.General, nodes.Element):
    pass



def html_hover_visit(self,node):
    # If HTML is to be generated, append the code.
    self.body.append(node['code'])

def html_hover_depart(self,node):
    pass

def tex_hover_visit(self,node):
    pass

def tex_hover_depart(self,node):
    # If TEX code is to be generated, append 'word' in italic.
    self.body.append("\\textit{"+node['word']+"}")
    

def setup(app):
    # Extension setup.
    app.add_node(hover, html = (html_hover_visit, html_hover_depart), latex = (tex_hover_visit, tex_hover_depart))
    app.add_role('hover',hover_role)