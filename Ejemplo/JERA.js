
/* Global variables */
var errorOccured = false;

function error() {
  errorOccured = true;
  document.getElementById("message").innerHTML = "Unable to load model or tracker!";
}

function createTracker(){

  // create tracker 
  var trackerDataSetPath = "./assets/tracker/Wikitude_Logos.zip";
  var Tracker = new AR.Tracker(trackerDataSetPath, { onLoaded : trackerLoaded, onError: error });
  
 
  // create the Model
  var ID_OBJ_1 = new AR.Model("./assets/models/model.wt3", {
    scale : {
        x : 1,
        y : 1,
        z : 1
    },
    rotate : {
        tilt :    0,
        heading : 0,
        roll :    0
    },
    translate : {
        x : 0,
        y : 0,
        z : 0
    },
    enabled : true
  });


  //start the model animation when the trackable comes into the field of vision
  var trackableOnEnterFieldOfVision = function(){
      ID_OBJ_1.enabled = true;
  }
  
  //disable the model when the Trackable is invisible
  var trackableOnExitFieldOfVision = function(){
      ID_OBJ_1.enabled = false;
    }
  
  var trackable2DObject = new AR.Trackable2DObject(Tracker, "Wikitude_Logo_SeeMore", {
      drawables: { cam: [ID_OBJ_1] },
      onEnterFieldOfVision : trackableOnEnterFieldOfVision,
      onExitFieldOfVision : trackableOnExitFieldOfVision
  });
    
}

function trackerLoaded()
{
  if (errorOccured) return;

  document.getElementById("message").style.display = "none";
}

$(document).ready(function(){
    createTracker();
})

    