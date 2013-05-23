#!/usr/bin/python

import sys

states = (('tag','exclusive'),('attr','exclusive'),('attr1','exclusive'),)

reserved = {'scene':'SCENE','manifest':'MANIFEST','object':'OBJECT','button':'BUTTON'}

tokens = ['TAGOPEN','TAGCLOSEOPEN','TAGCLOSE','TAGLONE','ATTRS','ATTRASSIGN','ATTRVALOPEN','ATTRVALSTR','ATTRVALCLOSE','ATTRVALOPEN1','ATTRVALSTR1','ATTRVALCLOSE1',] + list(reserved.values())

t_ignore  = ' \t\r'


def t_TAGCLOSEOPEN(t):
	r'</'
	t.lexer.push_state('tag')
	return t
	
def t_TAGOPEN(t):
	r'<'
	t.lexer.push_state('tag')
	return t
	
t_tag_ignore = ' \t\r\n'

def t_tag_ATTRS(t):
	r'[a-zA-Z_0-9]+'
	t.type = reserved.get(t.value,'ATTRS')
	return t
	
def t_tag_TAGCLOSE(t):
	r'>'
	t.lexer.pop_state()
	return t
	
def t_tag_TAGLONE(t):
	r'/>'
	t.lexer.pop_state()
	return t
	
t_tag_ATTRASSIGN = r'='

def t_tag_ATTRVALOPEN(t):
	r'\''
	t.lexer.push_state('attr')
	return t

def t_tag_ATTRVALOPEN1(t):
	r'\"'
	t.lexer.push_state('attr1')
	return t
	
#ATRIBUTOS CON '

t_attr_ignore = ' \t\r'

def t_attr_ATTRVALSTR(t):
	r'[^\']+'
	return t

def t_attr_ATTRVALCLOSE(t):
	r'\''
	t.lexer.pop_state()
	return t

#ATRIBUTOS CON "

t_attr1_ignore = ' \t\r'

def t_attr1_ATTRVALSTR1(t):
	r'[^\"]+'
	return t

def t_attr1_ATTRVALCLOSE1(t):
	r'\"'
	t.lexer.pop_state()
	return t

def t_newline(t):
	r'[\n]'
	t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print "Error: '"+str(t.value[0])+"' en Linea "+ str(t.lexer.lineno)+" en La Columna"+str(find_column(data,t))
    t.lexer.skip(1)
	
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    if last_cr == 0:
	column = 1
    else:
    	column = (token.lexpos - last_cr)
    return column
	
import lex

pila_tag = [] #en caso de emergencia rompa el vidrio
start = 'tag'

def p_tag(p):
	'''tag : simpletag
		| lonetag
	'''
	print p[1]
		
def p_simpletag(p):
	'''simpletag : opentag child closetag'''
	p[0] = p[1] + p[2] + p[3]
	
def p_opentag(p):
	'''opentag : TAGOPEN tagname attrs TAGCLOSE'''
	p[0] = p[1] + p[2] + p[3] + p[4]

def p_closetag(p):
	'''closetag : TAGCLOSEOPEN tagname TAGCLOSE'''
	p[0] = p[1] + p[2] + p[3]
	
def p_lonetag(p):
	'''lonetag : TAGOPEN tagname attrs TAGLONE'''
	p[0] = p[1] + p[2] + p[3] + p[4]
	
def p_tagname(p):
	'''tagname : SCENE
		| MANIFEST
		| OBJECT
		| BUTTON'''
	p[0] = p[1]
	
def p_attrs(p):
	'''attrs : ATTRS ATTRASSIGN atributo attrs
		| lambda'''
	if len(p) != 2:
		p[0] = ' ' + str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])
	else:
		p[0] = ''

def p_atributo(p):
	'''atributo : ATTRVALOPEN ATTRVALSTR ATTRVALCLOSE
		| ATTRVALOPEN1 ATTRVALSTR1 ATTRVALCLOSE1
	'''
	p[0] = p[1] + p[2] + p[3]
	
def p_child(p):
	'''child : child children 
		| lambda'''
	if len(p) > 2:
		if p[2]:
			p[0] = p[1] + p[2]
		else:
			p[0] = p[1]
	else:
		p[0] = ''
	
def p_children(p):
	'''children : tag'''
	p[0] = p[1]
	
def p_lambda(p):
	'lambda : '
	
def p_error(p):
	print 'Error de sintaxis ' + str(p)
	pass

import yacc	
data = ''

if len(sys.argv) == 2 :
	inputFile = sys.argv[1]
else:
	quit()
	
data = open(inputFile,'r').read()

lexer = lex.lex()
parser = yacc.yacc()
a = parser.parse(data,tracking=True)
