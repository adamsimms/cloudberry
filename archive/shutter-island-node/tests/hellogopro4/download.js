// Download and delete an image from GoPro
// Angela Gabereau
// Sun Aug 6 2017 00:33 NFLD STD
// @ Studeerochee MTL

// Prerequiste: GoPro4 Camera is paired, and wifi is on
// Actions:
// - Powers on GoPro4
// - Download last image
// - Delete last image
// - Powers off GoPro4

var lastDirectory,lastFile,newFilePath,
shutterBoxPath = "/home/pi/ShutterIsland/ShutterBox",
GoPro = require('goproh4'),
cam = new GoPro.Camera({
    mac: 'D4:D9:19:9A:00:5A'
});

console.log("Download and delete an image from GoPro");

cam.ready()
.then(function () {
    cam.powerOn();
})
.delay(6000)
.then(function () {
    cam.listMedia().then(function (result) {
        lastDirectory = result.media[result.media.length - 1];
        lastFile = lastDirectory.fs[lastDirectory.fs.length - 1];
	newFilePath = shutterBoxPath + "/something_meaningful_" + lastFile.n;
        cam.getMedia(lastDirectory.d, lastFile.n, newFilePath).then(function (filename) {
            console.log(filename, '[saved]');
	    // Now delete what you just dowloaded
	    cam.deleteLast().then(function () {
    		console.log('[last media deleted]');
		});
        });
     });

});
