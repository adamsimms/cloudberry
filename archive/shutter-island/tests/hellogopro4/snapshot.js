var GoPro = require('goproh4');

//var cam = new GoPro.Camera();
var cam = new GoPro.Camera({
    mac: 'D4:D9:19:9A:00:5A'
});

console.log("Taking a snapshot");

// Set camera mode
cam.mode(GoPro.Settings.Modes.Photo, GoPro.Settings.Submodes.Photo.Single)

// Set photo resolution
.then(function () {
    return cam.set(GoPro.Settings.PHOTO_RESOLUTION, GoPro.Settings.PhotoResolution.R7MPMedium);
})

// Take picture
.then(function () {
    return cam.start()
})

// Done
.then(function () {
    console.log('[picture taken]')
});
