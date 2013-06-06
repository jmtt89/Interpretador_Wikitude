
/* Global variables */
var errorOccured = false;

function error() {
  errorOccured = true;
  document.getElementById("message").innerHTML = "Unable to load model or tracker!";
}

function createTracker(){

  // create tracker 
  var trackerDataSetPath = "./assets/tracker/Prueba.zip";
  var Tracker = new AR.Tracker(trackerDataSetPath, { onLoaded : trackerLoaded, onError: error });
  
 
  // create the Model
  var Flyer = new AR.Model("./assets/models/flyer.wt3", {
    scale : {
        x : 0.01,
        y : 0.01,
        z : 0.01
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
      Flyer.enabled = true;
  }
  
  //disable the model when the Trackable is invisible
  var trackableOnExitFieldOfVision = function(){
      Flyer.enabled = false;
    }
  
  var trackable2DObject = new AR.Trackable2DObject(Tracker, "LogoCentral", {
      drawables: { cam: [Flyer] },
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

     
function errorAnimation() {
	document.getElementById("message").innerHTML = "Error Animation";
}
	