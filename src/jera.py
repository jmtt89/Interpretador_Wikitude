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
    p[0] = p[1]
        
def p_simpletag(p):
    '''simpletag : opentag child closetag'''
    p[1]['manifest'] += p[2]['manifest']
    p[1]['objects']  += p[2]['objects']
    p[1]['buttons']  += p[2]['buttons']
    p[0] = p[1]
#    p[0] = p[1] + p[2] + p[3]
    
def p_opentag(p):
    '''opentag : TAGOPEN tagname attrs TAGCLOSE'''
    p[0] = {'manifest':[],'objects':[],'buttons':[]}
    if p[2] == 'manifest':
        p[0]['manifest'] += [p[3]]
    elif p[2] == 'object':
        p[0]['objects'] += [p[3]]
    elif p[2] == 'button':
        p[0]['buttons'] += [p[3]]
#    p[0] = p[1] + p[2] + p[3] + p[4]

def p_closetag(p):
    '''closetag : TAGCLOSEOPEN tagname TAGCLOSE'''
#    p[0] = p[1] + p[2] + p[3]
    
def p_lonetag(p):
    '''lonetag : TAGOPEN tagname attrs TAGLONE'''
    p[0] = {'manifest':[],'objects':[],'buttons':[]}
    if p[2] == 'manifest':
        p[0]['manifest'] += [p[3]]
    elif p[2] == 'object':
        p[0]['objects'] += [p[3]]
    elif p[2] == 'button':
        p[0]['buttons'] += [p[3]]

#    p[0] = p[1] + p[2] + p[3] + p[4]
    
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
        aux = {str(p[1]):str(p[3])}
        aux.update(p[4])
        p[0] = aux
    else:
        p[0] = {}

def p_atributo(p):
    '''atributo : ATTRVALOPEN ATTRVALSTR ATTRVALCLOSE
        | ATTRVALOPEN1 ATTRVALSTR1 ATTRVALCLOSE1
    '''
    p[0] = p[2]
#    p[0] = p[1] + p[2] + p[3]
    
def p_child(p):
    '''child : child children 
        | lambda'''
    if len(p) > 2:
        if p[2]:
            p[2]['manifest'] += p[1]['manifest']
            p[2]['objects']  += p[1]['objects']
            p[2]['buttons']  += p[1]['buttons']
            p[0] = p[2]
    else:
        p[0] = {'manifest':[],'objects':[],'buttons':[]}
    
def p_children(p):
    '''children : tag'''
    p[0] = p[1]
    
def p_lambda(p):
    'lambda : '
    
def p_error(p):
    print 'Error de sintaxis ' + str(p)
    pass
#########################################
### Generar el HTML , CSS y JS

def Documentos(manifest,objetos,botones):
    html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
        <meta name="Description" content="'''+manifest['description']+'''" >
        <title>'''+manifest['title']+'''</title>

        <!-- Tamano de la Pantalla -->
        <meta name="viewport" content="target-densitydpi=device-dpi, width = 540, user-scalable = 0" />

        <!-- CSS Styles -->

            <!-- CSS Bootstrap_Twitter -->
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/bootstrap-responsive.min.css">

            <!-- CSS JERA -->
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/JERA.css">


            <!-- CSS para el Usuario -->
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/My.css">


        <!-- JavaScript -->
            <!-- Include the ARchitect library -->
            <script src="architect://architect.js"></script>

            <!-- Include the ARchitect Desktop Engine for testing on a desktop browser-->
            <script type="text/javascript" src="./assets/javascript/ade.js"></script>

            <!-- JavaScript Bootstrap_Twitter -->
            <script type="text/javascript" src="./assets/javascript/bootstrap.min.js"></script>

            <!-- JavaScript JERA -->
            <script type="text/javascript" src="./assets/javascript/JERA.js"></script>

            <!-- JavaScript para el Usuario -->
            <script type="text/javascript" src="./assets/javascript/My.js"></script>
    </head>

    <body>
        <div id="message"></div>
    '''
    for boton in botones:
        html+='''
            <a id="'''+boton['id']+'''" class="btn btn-'''+boton['type']+'''"></a>
        '''

    html+='''
    </body>
</html>
    '''

        

    js = '''
/* Global variables */
var errorOccured = false;

function error() {
  errorOccured = true;
  document.getElementById("message").innerHTML = "Unable to load model or tracker!";
}

function createTracker(){

  // create tracker 
  var trackerDataSetPath = "./assets/tracker/'''+manifest['tracker']+'''";
  var Tracker = new AR.Tracker(trackerDataSetPath, { onLoaded : trackerLoaded, onError: error });
  
'''
    for objeto in objetos:
        [tx,ty,tz] = objeto['position'].split()
        [rx,ry,rz] = objeto['rotation'].split()
        [sx,sy,sz] = objeto['scale'].split()
        js+=''' 
  // create the Model
  var '''+objeto['id']+''' = new AR.Model("./assets/models/'''+objeto['source']+'''", {
    scale : {
        x : '''+sx+''',
        y : '''+sy+''',
        z : '''+sz+'''
    },
    rotate : {
        tilt :    '''+rx+''',
        heading : '''+ry+''',
        roll :    '''+rz+'''
    },
    translate : {
        x : '''+tx+''',
        y : '''+ty+''',
        z : '''+tz+'''
    },
    enabled : '''+objeto['visible']+'''
  });


  //start the model animation when the trackable comes into the field of vision
  var trackableOnEnterFieldOfVision = function(){
      '''+objeto['id']+'''.enabled = true;
  }
  
  //disable the model when the Trackable is invisible
  var trackableOnExitFieldOfVision = function(){
      '''+objeto['id']+'''.enabled = false;
    }
  
  var trackable2DObject = new AR.Trackable2DObject(Tracker, "'''+objeto['target']+'''", {
      drawables: { cam: ['''+objeto['id']+'''] },
      onEnterFieldOfVision : trackableOnEnterFieldOfVision,
      onExitFieldOfVision : trackableOnExitFieldOfVision
  });
    '''

    js += '''
}

function trackerLoaded()
{
  if (errorOccured) return;

  document.getElementById("message").style.display = "none";
}
    '''
  
  
  
    css = ' '
    for boton in botones:
        [x,y] = boton['position'].split()
        css+= '#'+boton['id']+'{ position: absolute;top:  '+x+'px; left: '+y+'px; }'

    F_HTML = open("index.html","w")
    F_JS = open("JERA.js","w")
    F_CSS = open("JERA.css","w")

    F_HTML.write(html)
    F_JS.write(js)
    F_CSS.write(css)




################# MAIN ##################
import yacc 
data = ''

if len(sys.argv) == 2 :
    inputFile = sys.argv[1]
else:
    quit()
    
data = open(inputFile,'r').read()

lexer = lex.lex()
parser = yacc.yacc()
Res = parser.parse(data,tracking=True)

manifest = Res['manifest'][0]
objects = Res['objects']
buttons =Res['buttons']

Documentos(manifest,objects,buttons)

import os
import shutil
directorio_base = os.path.join('./public_html')
directorio_assets = os.path.join('./public_html/assets')
directorio_images = os.path.join('./public_html/assets/images')
directorio_javascript = os.path.join('./public_html/assets/javascript')
directorio_stylesheet = os.path.join('./public_html/assets/stylesheet')
directorio_tracker = os.path.join('./public_html/assets/tracker')
directorio_models = os.path.join('./public_html/assets/models')

if os.path.isdir(directorio_base):
    shutil.rmtree(directorio_base, 'true')

os.mkdir(directorio_base)
os.mkdir(directorio_assets)
os.mkdir(directorio_images)
os.mkdir(directorio_javascript)
os.mkdir(directorio_stylesheet)
os.mkdir(directorio_tracker)
os.mkdir(directorio_models)
open("My.js","w")
open("My.css","w")
shutil.copy2('./'+manifest['tracker'], './public_html/assets/tracker')
for objeto in objects:
    shutil.copy2('./'+objeto['source'], './public_html/assets/models')

shutil.copy2('./JERA.js', './public_html/assets/javascript')
shutil.copy2('./My.js', './public_html/assets/javascript')
shutil.copy2('../ADE/ade.js', './public_html/assets/javascript')
shutil.copy2('../bootstrap_Twitter/js/bootstrap.min.js', './public_html/assets/javascript')

shutil.copy2('./JERA.css', './public_html/assets/stylesheet')
shutil.copy2('./My.css', './public_html/assets/stylesheet')
shutil.copy2('../bootstrap_Twitter/css/bootstrap-responsive.min.css', './public_html/assets/stylesheet')
shutil.copy2('../bootstrap_Twitter/css/bootstrap.min.css', './public_html/assets/stylesheet')

shutil.copy2('../bootstrap_Twitter/img/glyphicons-halflings-white.png', './public_html/assets/images')
shutil.copy2('../bootstrap_Twitter/img/glyphicons-halflings.png', './public_html/assets/images')

shutil.copy2('./index.html', './public_html')

