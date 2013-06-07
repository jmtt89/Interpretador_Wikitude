////////////////////////////////////////////
//////// Traduccion de Scale ///////////////
////////////////////////////////////////////

//
// <Nombre del ID si esta asignado>_<Eje>
//   |
//   v
var trans_5_X = new AR.PropertyAnimation(
  Flyer, //<<-- ID del Target
  "scale.x", //<<-- Propiedad a modificar
  0.01, //<<-- Inicial
  0.02, //<<-- Final
  1000, //<<-- Duracion
  {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}, //<<-- Tipo de Interpolacion
);

var trans_5_Y = new AR.PropertyAnimation(
  Flyer, //<<-- ID del Target
  "scale.y", //<<-- Propiedad a modificar
  0.01, //<<-- Inicial
  0.02, //<<-- Final
  1000, //<<-- Duracion
  {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}, //<<-- Tipo de Interpolacion
);

var trans_5_Z = new AR.PropertyAnimation(
  Flyer, //<<-- ID del Target
  "scale.z", //<<-- Propiedad a modificar
  0.01, //<<-- Inicial
  0.02, //<<-- Final
  1000, //<<-- Duracion
  {type: AR.CONST.EASING_CURVE_TYPE.LINEAR}, //<<-- Tipo de Interpolacion
);

//
// <Nombre del ID si esta asignado>
//   |
//   v
var trans_5 = new AR.AnimationGroup(
  AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL, // <<-- siempre una transition es una parallel de X,Y,Z sobre el campo que se quiera
  [trans_5_X,trans_5_Y,trans_5_Z], // <<-- las animaciones creadas arriba
);

