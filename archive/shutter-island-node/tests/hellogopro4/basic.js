var GoPro = require('goproh4');
//var cam = new GoPro.Camera();

var cam = new GoPro.Camera({
    mac: 'D4:D9:19:9A:00:5A'
});


console.log("hello goproh4");
console.log(cam);


cam.ready()
.then(function () {
  console.log(cam);
  console.log("Camera REady!!");
});
