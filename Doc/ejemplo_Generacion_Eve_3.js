var Animations = {}

function LoadAnim(){

  var trans_5_X = new AR.PropertyAnimation(
    Flyer, 
    "scale.x", 
    0.01, 
    0.02, 
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_5_Y = new AR.PropertyAnimation(
    Flyer,
    "scale.y",
    0.01,
    0.02,
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_5_Z = new AR.PropertyAnimation(
    Flyer,
    "scale.z",
    0.01,
    0.02,
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_5 = new AR.AnimationGroup(
    AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL,
    [trans_5_X,trans_5_Y,trans_5_Z],
  );

  var trans_6_X = new AR.PropertyAnimation(
    Flyer, 
    "rotation.x", 
    0, 
    90, 
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_6_Y = new AR.PropertyAnimation(
    Flyer,
    "rotation.y",
    0,
    180,
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_6_Z = new AR.PropertyAnimation(
    Flyer,
    "rotation.z",
    0,
    90,
    1000,
    {type: AR.CONST.EASING_CURVE_TYPE.LINEAR},
  );

  var trans_6 = new AR.AnimationGroup(
    AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL,
    [trans_6_X,trans_6_Y,trans_6_Z],
  );

  Animations['EVE_3'] = new AR.AnimationGroup(
                          AR.CONST.ANIMATION_GROUP_TYPE.PARALLEL,
                          [trans_5,trans_6]
                        );

  
}