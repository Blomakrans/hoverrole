# -*- coding: UTF-8-sig -*-

# The role :hover:`word,term` provides an inline highlight of 'word' with a mouse-over 
# translation from Icelandic to English of 'term' according to the stae.is/os database.
# In the case of :hover:`word`. The string 'term' is assumed to be the same as 'word'

# Author: Símon Böðvarsson
# 29.06.2016

from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes
import ordaskra
import time

def hover_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    # app lets us access configuration settings and the parser as well as save
    # data for later use.
    app = inliner.document.settings.env.app
    #dictFile = app.config.hover_dictFile
    transNum = app.config.hover_numOfTranslations
    htmlLink = app.config.hover_htmlLinkToStae
    latexLink = app.config.hover_latexLinkToStae
    latexIt = app.config.hover_latexItText

    # for text input of the form: "word,term"
    try:
        [word,term] = text.split(",")
    # If no 'term' is provided, it is assumed to be the same as 'word'.
    except ValueError: 
        word=term=text

    node = make_hover_node(word,term,transNum,htmlLink,latexLink,latexIt)
    return [node],[]

def make_hover_node(word,term,transNum,htmlLink,latexLink,latexIt):
     # Create new hover object.
    hover_node = hover()
    hover_node['word'] = word

    # Get English translation of Icelandic term.
    translation = ordaskra.isTranslate(term,transNum)
    # Get first translation
    try:
        singleTranslation = translation[0][0]
    except:
        singleTranslation = ""

    # Get all translations and add to string.
    tranStr = ''
    lastStr = ''
    for item in translation:
        # Skip repeated translations
        if ''+item[0] == lastStr:
            pass
        else:
            tranStr = tranStr + item[0] + ", "
            lastStr = item[0]
    allTranslation = tranStr[:-2] + "."

    # If no translation was found, append error message instead of translation.
    if allTranslation == ".":
        errorMsg = u'Ekki fannst þýðing á hugtakinu: ' 
        codebit = '<a class="tooltip" target="_blank">'+word+'<span><staelink style="line-height:4px; font-size:80%;">'+errorMsg+'<i>'+term+'</i></staelink></span></a>'

    # Else construct the tooltip according to the user-settings.
    else:
        codebit = '<a '
        if htmlLink:
            codebit = codebit + 'href="http://www.stae.is/os/leita/'+unicode(singleTranslation.replace(" ","_")) 
        if transNum == 'single':
            codebit = codebit + '" class="tooltip" target="_blank">'+word+'<span>en: <i>'+unicode(singleTranslation)+u'</i>'
        else: 
            codebit = codebit + '" class="tooltip" target="_blank">'+word+'<span>en: <i>'+unicode(allTranslation)+u'</i>'
        if htmlLink:
            codebit = codebit + u'<staelink style="font-size:80%;"><br><strong>Smelltu</strong> fyrir ítarlegri þýðingu.</staelink>'
        codebit = codebit + '</span></a>'

    # Generate latex code based on conf.py options.
    latexCode = unicode(word)
    if latexIt:
        latexCode = '\\textit{' + latexCode + '}'
    if latexLink:
        urlTerm = singleTranslation.rstrip()
        searchURL = 'http://www.stae.is/os/leita/'+unicode(urlTerm.replace(" ","\_"))
        latexCode = '\\href{' + searchURL +'}{' + word +'}'


    # Add the HTML and Latex code snippets to the node.
    hover_node['latexcode'] = latexCode
    hover_node['htmlcode'] = codebit
    
    return hover_node

class hover(nodes.General, nodes.Element):
    pass

def html_hover_visit(self,node):
    self.body.append(node['htmlcode'])

def html_hover_depart(self,node):
    pass

def tex_hover_visit(self,node):
    pass

def tex_hover_depart(self,node):
    self.body.append(node['latexcode'])

def setup(app):
    # Extension setup.

    # Name of dictionary file to be used without .py (default 'staeOrdasafn').
    #app.add_config_value('hover_dictfile','staeOrdasafn','html')
    
    # Number of translations to be displayed. The default 'single' displays only
    # the first translation, 'all' displays all found translations.
    app.add_config_value('hover_numOfTranslations','single','html')
    # Set to default ('1') if hover target should link to stae.is search for the translated term.
    # Set to '0' if no link should be attached.
    app.add_config_value('hover_htmlLinkToStae',1,'html')
    app.add_config_value('hover_latexLinkToStae',0,'env')
    # Should the text be italicized in latex output. '1' for on, '0' for off.
    app.add_config_value('hover_latexItText',1,'env')

    app.add_node(hover, html = (html_hover_visit, html_hover_depart), latex = (tex_hover_visit, tex_hover_depart))
    app.add_role('hover',hover_role)