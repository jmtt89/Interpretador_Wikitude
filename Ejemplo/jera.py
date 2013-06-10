#!/usr/bin/python

import sys

states = (('tag','exclusive'),('attr','exclusive'),('attr1','exclusive'),)

reserved = {'scene':'SCENE','manifest':'MANIFEST','object':'OBJECT','button':'BUTTON','group':'GROUP','play':'PLAY','event':'EVENT','sequence':'SEQUENCE','parallel':'PARALLEL','transition':'TRANSITION','audio':'AUDIO','set':'SET','toggle':'TOGGLE'}

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
    print "Error: '"+str(t.value[0])+"' en Linea "+ str(t.lexer.lineno)+" en La Columna "+str(find_column(data,t))
    t.lexer.skip(1)
    sys.exit()
    
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
pila_tag_to_validate = []
common_attr = ['id','visible','translate']
manifest_attr_req = ['title','description','tracker']
object_attr_req = common_attr + ['scale','rotate','source','target']
button_attr_req = common_attr + ['type','text','size']

import re

def is_valid_attr(attrs,values,lista):
    if len(attrs) != len(lista):
        print 'Error: Falta atributo requerido'
        sys.exit()
    for (e1,e2) in zip(attrs,values):
        if not(e1 in lista):
            print 'Error: Atributo inesperado "' + e1 +'"'
            sys.exit()
        if (attrs.count(e1) != 1):
            print 'Error: Atributo repetido "'+e1+'"'
            sys.exit()
        validate_value(e1,e2)

def validate_value(tipo,valor):
    if tipo == 'visible':
        if re.match(r'(true|false)',valor):
            return
    elif tipo == 'translate':
        if re.match(r'\d+[ ]+\d+[ ]+\d+',valor) or re.match(r'\d+[ ]+\d+',valor):
            return
    elif tipo == 'type':
        if re.match(r'(default|primary|info|success|danger|warning|inverse)',valor):
            return
    elif tipo == 'rotate' or tipo == 'scale':
        if re.match(r'\d+[ ]+\d+[ ]+\d+',valor):
            return
    elif tipo == 'size':
        if re.match(r'\d+',valor):
            return
    elif tipo == 'tracker' or tipo == 'description' or tipo == 'id' or tipo == 'title' or tipo == 'source' or tipo == 'target' or tipo == 'text':
        if re.match(r'[a-zA-Z_0-9]+',valor):
            return
    print 'Error: valor de atributo invalido "' + valor + '"'
    sys.exit()

start = 'tag'

def p_tag(p):
    '''tag : simpletag
        | lonetag
    '''
    p[0] = p[1]
        
def p_simpletag(p):
    '''simpletag : opentag child closetag'''
    p[1].hijos = p[2]
    p[0] = p[1]
#    p[0] = p[1] + p[2] + p[3]
    
def p_opentag(p):
    '''opentag : TAGOPEN tagname attrs TAGCLOSE'''
    p[0] = Dom.Element(p[2],p[3])
#    p[0] = p[1] + p[2] + p[3] + p[4]

def p_closetag(p):
    '''closetag : TAGCLOSEOPEN tagname TAGCLOSE'''
    
def p_lonetag(p):
    '''lonetag : TAGOPEN tagname attrs TAGLONE'''
    p[0] = Dom.Element(p[2],p[3])
    
def p_tagname(p):
    '''tagname : SCENE
        | MANIFEST
        | OBJECT
        | BUTTON
		| EVENT
		| AUDIO
		| SET
		| SEQUENCE
        | PARALLEL
		| TRANSITION
		| PLAY
        | TOGGLE'''
    p[0] = p[1]
    
def p_attrs(p):
    '''attrs : ATTRS ATTRASSIGN atributo attrs
        | lambda'''
    if len(p) != 2:
        pila_tag.append(str(p[1]))
        pila_tag_to_validate.append(str(p[3]))
        aux = {str(p[1]):str(p[3])}
        aux.update(p[4])
        p[0] = aux
    else:
        del pila_tag[0:len(pila_tag)]
        del pila_tag_to_validate[0:len(pila_tag_to_validate)]
        p[0] = {}

def p_atributo(p):
    '''atributo : ATTRVALOPEN ATTRVALSTR ATTRVALCLOSE
        | ATTRVALOPEN1 ATTRVALSTR1 ATTRVALCLOSE1
    '''
    p[0] = p[2]
    
def p_child(p):
    '''child : child children 
        | lambda'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []
    
def p_children(p):
    '''children : tag'''
    p[0] = p[1]
    
def p_lambda(p):
    'lambda : '
    
def p_ANY_error(p):
    print 'Error de sintaxis ' + str(p)
    pass

#########################################
### Clase de Arbol

class Dom:
    class Element:
        def __init__(self,nombre, attr = {}, hijos = []):
            self.nombre = nombre
            self.attributos = attr
            self.hijos = hijos

        def __str__(self):
            attributes_str = ''
            for attr in self.attributos:
                attributes_str += ' %s="%s"' % (attr, self.attributos[attr])

            children_str = ''
            for child in self.hijos:
                if isinstance(child, self.__class__):
                    children_str += str(child)
                else:
                    children_str += child

            return '<%s %s>\n%s\n</%s>'% (self.nombre, attributes_str, children_str, self.nombre)
            
        def __repr__(self):
            return str(self)

#########################################
### Generar el HTML , CSS y JS

def Documentos(Arbol):

    manifest = Find(Arbol,'manifest')[0]
    botones  = Find(Arbol,'button')
    modelos  = Find(Arbol,'object')
    audios   = Find(Arbol, 'audio')
    Events   = Childrens(Arbol,'event')
    Buttons  = Childrens(Arbol,'button')
    Models   = Childrens(Arbol,'object')

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
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/bootstrap.css">
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/bootstrap-responsive.css">

            <!-- CSS JERA -->
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/JERA.css">


            <!-- CSS para el Usuario -->
            <link rel="stylesheet" type="text/css" href="./assets/stylesheet/My.css">


        <!-- JavaScript -->
            <!-- Include the ARchitect library -->
            <script src="architect://architect.js"></script>

            <!-- Include the ARchitect Desktop Engine for testing on a desktop browser-->
            <script type="text/javascript" src="./assets/javascript/ade.js"></script>

            <!-- JavaScript JQuery -->
            <script type="text/javascript" src="./assets/javascript/jquery-1.9.1.min.js"></script>                

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
            <a id="'''+boton['id']+'''" class="btn btn-'''+boton['type']+'''">'''+boton['text']+'''</a>
        '''

    html+='''
    </body>
</html>
    '''

        

    js = '''
/* Global variables */
var errorOccured = false;
var Models = {}

function error() {
  errorOccured = true;
  document.getElementById("message").innerHTML = "Unable to load model or tracker!";
}

function createTracker(){

  // create tracker 
  var trackerDataSetPath = "./assets/tracker/'''+manifest['tracker']+'''";
  var Tracker = new AR.Tracker(trackerDataSetPath, { onLoaded : trackerLoaded, onError: error });
  
'''
###############################   Cargar Modelos  ###########################################
#############################################################################################

    for modelo in modelos:
        [tx,ty,tz] = modelo['translate'].split()
        [rx,ry,rz] = modelo['rotate'].split()
        [sx,sy,sz] = modelo['scale'].split()
        js+=''' 

  // create the Model
  var '''+modelo['id']+''' = new AR.Model("./assets/models/'''+modelo['source']+'''", {
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
    enabled : '''+modelo['visible']+''',
    onClick : function(){
        //Si existen Eventos Asociados a un on click de modelo generar aqui
    }

    
    
  });
    
    Models["'''+modelo['id']+'''"] = '''+modelo['id']+'''   

  //Habilitar el modelo cuando entra en el campo de Vision
  var trackableOnEnterFieldOfVision = function(){
      '''+modelo['id']+'''.enabled = true;
  }
  
  //Desabilitar el modelo cuando sale del campo de Vision
  var trackableOnExitFieldOfVision = function(){
      '''+modelo['id']+'''.enabled = false;
    }
  
  var trackable2DObject = new AR.Trackable2DObject(Tracker, "'''+modelo['target']+'''", {
      drawables: { cam: ['''+modelo['id']+'''] },
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


###################### Cargar Animaciones #################################
###########################################################################
    js += ''' 
function errorAnimation() {
    document.getElementById("message").innerHTML = "Error Animation";
}

var Animations = {}

function LoadAnim(){
    
    function CreateTransition(Atributos){

        var What;
        if (Atributos['what'] != 'rotate') { 
            What = {x:Atributos['what']+".x",y:Atributos['what']+".y",z:Atributos['what']+".z"};
        } else { 
            What = {x:Atributos['what']+".tilt",y:Atributos['what']+".heading",z:Atributos['what']+".roll"};
        } 

        var X = new AR.PropertyAnimation(
            Models[Atributos['target']],
            What['x'],
            Atributos['sx'], 
            Atributos['ex'], 
            Atributos['duration'],
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
            );

        var Y = new AR.PropertyAnimation(
            Models[Atributos['target']], 
            What['y'],
            Atributos['sy'], 
            Atributos['ey'], 
            Atributos['duration'],
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
            );

        var Z = new AR.PropertyAnimation(
            Models[Atributos['target']], 
            What['z'],
            Atributos['sz'], 
            Atributos['ez'], 
            Atributos['duration'],
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
            );

        return new AR.AnimationGroup(
            AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL,
            [X,Y,Z]
        );
    }

    var Aux;
    var AnimArray = [];
    var AnimSeqnc = [];
        '''
### Donde Events son SubArboles y Event es un SubArbol Particular
    for Event in Events:
        js+='AnimSeqnc = [];'
        for Child in Event.hijos:
            
            if(Child.nombre == "transition"):
                [sx,sy,sz] = Child.attributos['start'].split()
                [ex,ey,ez] = Child.attributos['end'].split()   
                js+='''
    Aux = {target:"'''+Child.attributos['target']+'''",what:"'''+Child.attributos['what']+'''",sx:'''+sx+''',sy:'''+sy+''',sz:'''+sz+''',ex:'''+ex+''',ey:'''+ey+''',ez:'''+ez+''',duration:'''+Child.attributos['duration']+'''};
    AnimSeqnc.push(CreateTransition(Aux));
                '''
            
            if(Child.nombre == "sequence"):
                js+='''
    AnimArray = [];
                '''
                for transition in Child.hijos:
                    [sx,sy,sz] = transition.attributos['start'].split()
                    [ex,ey,ez] = transition.attributos['end'].split()                       
                    js+='''
    Aux = {target:"'''+transition.attributos['target']+'''",what:"'''+transition.attributos['what']+'''",sx:'''+sx+''',sy:'''+sy+''',sz:'''+sz+''',ex:'''+ex+''',ey:'''+ey+''',ez:'''+ez+''',duration:'''+transition.attributos['duration']+'''};
    AnimArray.push(CreateTransition(Aux));
                    '''
                js+='''
    AnimSeqnc.push(new AR.AnimationGroup(AR.CONST.ANIMATION_GROUP_TYPE.SEQUENTIAL,AnimArray));
                '''
            
            if(Child.nombre == "parallel"):
                js+='''
    AnimArray = [];
                '''
                for transition in Child.hijos:
                    [sx,sy,sz] = transition.attributos['start'].split()
                    [ex,ey,ez] = transition.attributos['end'].split()                       
                    js+='''
    Aux = {target:"'''+transition.attributos['target']+'''",what:"'''+transition.attributos['what']+'''",sx:'''+sx+''',sy:'''+sy+''',sz:'''+sz+''',ex:'''+ex+''',ey:'''+ey+''',ez:'''+ez+''',duration:'''+transition.attributos['duration']+'''};
    AnimArray.push(CreateTransition(Aux))
                    '''
                js+='''
    AnimSeqnc.push(new AR.AnimationGroup(AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL,AnimArray));
                '''

            if(Child.nombre == "set"):
                js+='''
    AnimSeqnc.push( new AR.PropertyAnimation(
            Models["'''+Child.attributos['target']+'''"],
            "translate.x",
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            1,
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
                '''
                if(Child.attributos['what'] == "visible"):
                    js+='''
            ,{ onFinish : function() { Models["'''+Child.attributos['target']+'''"].enabled = '''+Child.attributos['to']+'''; } }
                    '''
                js+='''
    ));
                '''

            if(Child.nombre == "toggle"):
                js+='''
    var '''+Child.attributos['id']+''' = Models["'''+Child.attributos['target']+'''"].enabled
    '''+Child.attributos['id']+''' = !'''+Child.attributos['id']+'''
    AnimSeqnc.push( new AR.PropertyAnimation(
            Models["'''+Child.attributos['target']+'''"],
            "translate.x",
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            1,
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
            ,{ onFinish : function() { Models["'''+Child.attributos['target']+'''"].enabled = '''+Child.attributos['id']+'''; } }
    ));
                '''

            if(Child.nombre == "play"):
                js+='''
    AnimSeqnc.push( new AR.PropertyAnimation(
            Models["'''+Child.attributos['target']+'''"],
            "translate.x",
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            Models["'''+Child.attributos['target']+'''"].translate.x, 
            1,
            {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}
            ,{ onFinish : function() { Sounds["'''+Child.attributos['start']+'''"].play(); } }
    ));
                '''



        js+='''
    Animations["'''+Event.attributos['id']+'''"] = new AR.AnimationGroup(AR.CONST.ANIMATION_GROUP_TYPE.SEQUENTIAL,AnimSeqnc);
        '''
    js+='''
}
    '''

    js+='''
    var Sounds = {}

    function LoadAudio(){
    '''
    for audio in audios:
        js+='''
    Sounds["'''+audio['id']+'''"] = new AR.Sound(
        "assets/sounds/'''+audio['filename']+'''"
        '''
        if audio['playonload'] == 'true':
            js+='''
            ,{onLoaded : function(){Sounds["'''+audio['id']+'''"].play();}}
            '''
        js+='''
        );
    
        Sounds["'''+audio['id']+'''"].load();
        '''
    js+='''
    }
    '''

    js+='''
$(document).ready(function(){
    createTracker();
    LoadAudio();
    LoadAnim();
});

$(document).ready(function(){
    '''

    for Model in Models:
        js+='''
    Models["'''+Model.attributos['id']+'''"].onClick = function(){
        '''
        for Event in Model.hijos:
            js+='''
        Animations["'''+Event.attributos['id']+'''"].start(1);
            '''
        js+='''
        }
        '''

    for Button in Buttons:
        js+='''
    $("'''+Button.attributos['id']+'''").click = function() {
        '''
        for Event in Button.hijos:
            js+='''
        Animations["'''+Event.attributos['id']+'''"].start(1);
            '''
        js+='''
    }
        '''
    js+='''
});
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

######################################################################
######################################################################
##############   Funciones Basicas sobre el Arbol ####################
######################################################################
######################################################################

### Lista de Atributos de un nodo con Id
def FindID(Arbol,ID):
    if ('id' in Arbol.attributos and Arbol.attributos['id'] == ID ):
        return Arbol.attributos
    else:
        for child in Arbol.hijos:
            tmp = FindID(child,ID)
            if(tmp):
                return tmp
        return False


### Lista de diccionario de Atributos de todos los nodos nodo Key
def Find(Arbol,key):
    Res = []
    FindAux(Arbol,key,Res)
    return Res

def FindAux(Arbol,key,Res):
    if (Arbol.nombre == key) :
        Res.append(Arbol.attributos)

    for child in Arbol.hijos:
       FindAux(child,key,Res)

### Lista con los SubArboles de un Key

def Childrens(Arbol,key):
    Res = []
    ChildrensAUX(Arbol,key,Res)
    return Res

def ChildrensAUX(Arbol,key,Res):
    if(Arbol.nombre == key):
        Res.append(Arbol)
   
    for Arb in Arbol.hijos:
        ChildrensAUX(Arb,key,Res)


#### Imprime el Arbol
def PrintArb(Arbol):
    str = Arbol.nombre + "|"
    for Child in Arbol.hijos:
        str += Child.nombre + ","
    str += '\n'
    for Child in Arbol.hijos:
        str += PrintArb(Child)

    return str

###################################################################
###################################################################
#################   Default Sobre el Arbol ########################
###################################################################
###################################################################

def Optional(Arbol,prop,val):
    if( not prop in Arbol.attributos ):
        Arbol.attributos[prop] = val


def AssingTarget(Arbol,target):
    if( not 'target' in Arbol.attributos ):
        Arbol.attributos['target'] = target

        for child in Arbol.hijos:
            AssingTarget(child,target)


def Assing_Auto_ID(Arbol):
    Assing_Auto_ID_AUX(Arbol,'event',0)
    Assing_Auto_ID_AUX(Arbol,'transition',0)
    Assing_Auto_ID_AUX(Arbol,'toggle',0)
    Assing_Auto_ID_AUX(Arbol,'play',0)


def Assing_Auto_ID_AUX(Arbol,key,index):
    if(Arbol.nombre == key and not 'id' in Arbol.attributos):
        Arbol.attributos['id'] = Arbol.nombre+"_"+str(index)

    inx = index
    for child in Arbol.hijos:
        inx += 1 
        Assing_Auto_ID_AUX(child,key,inx)

def Default (Arbol):
    Assing_Auto_ID(Arbol)
    DefaultAux(Arbol,Arbol)


def DefaultAux(ArbolCompleto,Arbol):

    if(Arbol.nombre == 'manifest'):
        Optional(Arbol,'title',"Aplicacion de Realidad Aumentada en JERA")
        Optional(Arbol,'description',"Aplicacion de Realidad Aumentada en JERA ")

    if(Arbol.nombre == 'object'):
        Optional(Arbol,'visible',"true")
        Optional(Arbol,'translate',"0 0 0")
        Optional(Arbol,'scale',"1 1 1")
        Optional(Arbol,'rotate',"0 0 0")
        for child in Arbol.hijos:
            AssingTarget(child,Arbol.attributos['id'])

    if(Arbol.nombre == 'event'):
        for child in Arbol.hijos:
            AssingTarget(child,Arbol.attributos['target'])

    if(Arbol.nombre == 'transition'):
        bsq = Arbol.attributos['what']
        lst = FindID(ArbolCompleto,Arbol.attributos['target'])
        Optional(Arbol,'start',lst[bsq])

    if(Arbol.nombre == 'button'):
        Optional(Arbol,'visible',"true")
        Optional(Arbol,'type',"default")
        Optional(Arbol,'size',"30")

    if(Arbol.nombre == 'audio'):
        Optional(Arbol,'playonload',"false")        

    for child in Arbol.hijos:
        DefaultAux(ArbolCompleto,child)


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


Default(Res)

Documentos(Res)



manifest = Find(Res,'manifest')[0]
objects  = Find(Res,'object')
audios   = Find(Res,'audio')

import os
import shutil
directorio_base = os.path.join('./public_html')
directorio_assets = os.path.join('./public_html/assets')
directorio_images = os.path.join('./public_html/assets/images')
directorio_audios = os.path.join('./public_html/assets/sounds')
directorio_javascript = os.path.join('./public_html/assets/javascript')
directorio_stylesheet = os.path.join('./public_html/assets/stylesheet')
directorio_tracker = os.path.join('./public_html/assets/tracker')
directorio_models = os.path.join('./public_html/assets/models')

if os.path.isdir(directorio_base):
    shutil.rmtree(directorio_base, 'true')

os.mkdir(directorio_base)
os.mkdir(directorio_assets)
os.mkdir(directorio_images)
os.mkdir(directorio_audios)
os.mkdir(directorio_javascript)
os.mkdir(directorio_stylesheet)
os.mkdir(directorio_tracker)
os.mkdir(directorio_models)
open("My.js","w")
open("My.css","w")
shutil.copy2('./'+manifest['tracker'], './public_html/assets/tracker')
for objeto in objects:
    shutil.copy2('./'+objeto['source'], './public_html/assets/models')
for audio in audios:
    shutil.copy2('./'+audio['filename'], './public_html/assets/sounds')
shutil.copy2('./JERA.js', './public_html/assets/javascript')
shutil.copy2('./My.js', './public_html/assets/javascript')
shutil.copy2('../ADE/ade.js', './public_html/assets/javascript')
shutil.copy2('../bootstrap_Twitter/js/bootstrap.js', './public_html/assets/javascript')
shutil.copy2('../Jquery/jquery-1.9.1.min.js', './public_html/assets/javascript')


shutil.copy2('./JERA.css', './public_html/assets/stylesheet')
shutil.copy2('./My.css', './public_html/assets/stylesheet')
shutil.copy2('../bootstrap_Twitter/css/bootstrap-responsive.css', './public_html/assets/stylesheet')
shutil.copy2('../bootstrap_Twitter/css/bootstrap.css', './public_html/assets/stylesheet')

shutil.copy2('../bootstrap_Twitter/img/glyphicons-halflings-white.png', './public_html/assets/images')
shutil.copy2('../bootstrap_Twitter/img/glyphicons-halflings.png', './public_html/assets/images')

shutil.copy2('./index.html', './public_html')

