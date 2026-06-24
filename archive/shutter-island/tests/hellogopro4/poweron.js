var GoPro = require('goproh4');
var cam = new GoPro.Camera({
    mac: 'D4:D9:19:9A:00:5A'
});
console.log("Turning on the camera");

cam.ready()
.then(function () {
    // Turn the camera on
    console.log("She back to life");
    console.log(cam)
    cam.powerOn();
});
