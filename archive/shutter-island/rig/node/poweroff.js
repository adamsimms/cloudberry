var GoPro = require('goproh4');
var cam = new GoPro.Camera({
    mac: 'D4:D9:19:9A:00:5A'
});
console.log("Turning off the camera");

cam.ready()
.then(function () {
    console.log("She be down");
    // Turn the camera off
    return cam.powerOff();
})