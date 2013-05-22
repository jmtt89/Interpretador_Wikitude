import sys

states = (('tag','exclusive'),('attr','exclusive'),)

reserved = {'scene':'SCENE','manifest':'MANIFEST','object':'OBJECT'}

tokens = ['TAGOPEN','TAGCLOSE','ATTRS','ATTRASSIGN','ATTRVAL','TAGNAME','TAGOPENEND','TAGCLOSEEND','ATTRVALSTR','ATTRVALCLOSE'] + list(reserved.values())

t_ignore  = ' \t\r'

def t_TAGOPEN(t):
	r'<'
	t.lexer.push_state('tag')
	return t

t_tag_ignore = ' \t\r'

def t_tag_ATTRS(t):
	r'[a-zA-Z_0-9]+'
	t.type = reserved.get(t.value,'ATTRS')
	return t
	
def t_tag_TAGOPENEND(t):
	r'>'
	t.lexer.pop_state();
	return t
	
def t_tag_TAGCLOSEEND(t):
	r'/>'
	t.lexer.pop_state()
	return t
	
t_tag_ATTRASSIGN = r'='

def t_tag_ATTRVAL(t):
	r'\''
	t.lexer.push_state('attr')
	return t

t_attr_ignore = ''
	
def t_attr_ATTRVALSTR(t):
	r'[^\']+'
	return t

def t_attr_ATTRVALCLOSE(t):
	r'\''
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

pila_salvadora = [] #en caso de emergencia rompa el vidrio


def p_init(p):
	'xml : tag'
	print(p[1])

def p_tag(p):
	'tag : opentag child closetag'
	p[0] = p[1]+p[2]+p[3]
	
def p_opentag(p):
	'opentag : TAGOPEN tagname attrs TAGOPENEND'
	p[0] = "< "+p[2]+p[3]+" >" 

def p_tagname(p):
	'''tagname : SCENE
		| MANIFEST
		| OBJECT'''
	p[0] = p[1]

		
def p_attrs(p):
	'''attrs : ATTRS ATTRASSIGN ATTRVAL ATTRVALSTR ATTRVALCLOSE attrs
		| lambda'''
	p[0] = p[1]+"="+"'"+p[4]+"' "

def p_closetag(p):
	'closetag : TAGOPEN tagname TAGCLOSEEND'
	p[0] = "< "+p[2]+" />" 

def p_child(p):
	'''child : tag
		| lambda'''
	p[0]=p[1]
	
def p_lambda(p):
	'lambda : '
	pass
	
def p_error(p):
	print 'Error de sintaxis'
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
a = parser.parse(data , tracking=True)