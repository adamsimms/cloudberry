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

var fs = require('fs'),
GoPro = require('goproh4'),
lastDirectory,lastFile,newFilePath,totalDownloadSize,
shutterBoxPath = "/home/pi/ShutterIsland/ShutterBox",
gCloudberryCam =  new GoPro.Camera({ mac: 'D4:D9:19:9A:00:5A' }),
powerOn = function() {
    var promise = new Promise(function(resolve, reject){
        return gCloudberryCam.ready()
        .then(function () {
            // Turn the camera on
            console.log('*** Powering on the Cloudberry GoPro ***');
            console.log(gCloudberryCam);
            gCloudberryCam.powerOn();
            console.log('*** Wait 6 seconds to it a chance to wake up ***');
        })
        .delay(6000)
        .then(function(){
            console.log("Should be ready to go by now");
            resolve("resolved powerOn");
        })
        .catch(function(fromReject){
            console.log('ERROR: powerOn caught a failure' + fromReject);
            reject(fromReject);
        });

    });
    return promise
},
powerOff = function() {
    var promise = new Promise(function(resolve, reject){
        return gCloudberryCam.ready()
        .then(function () {
            // Turn the camera on
            console.log('*** Powering off the Cloudberry GoPro ***');
            console.log(gCloudberryCam);
            gCloudberryCam.powerOff();
        })
        .then(function(){
            console.log("Should be off");
            resolve("resolved powerOff");
        })
        .catch(function(fromReject){
            console.log('ERROR: powerOff caught a failure' + fromReject);
            reject(fromReject);
        });

    });
    return promise
},
getImageFilename = function(directory, file) {
    var promise = new Promise(function(resolve, reject){
        console.log('*****getImageFilename promise *******');
        // console.log("directory");
        // console.log(directory);
        // console.log("file");
        // console.log(file);
     
        var dateTaken = new Date(file.mod * 1000); /* x1000 timestamp unix > timestamp ms */
        dateTaken = dateTaken.toISOString();
        // console.log("ISO dateTaken");
        // console.log(dateTaken);
        var size = file.s / 1000000; /* byte to mb */
        console.log("file size mb");
        console.log(size);
        var name = file.n; /* filename */
        // console.log("file name");
        // console.log(name);
        ////
        newFilePath = shutterBoxPath + "/" + dateTaken + '_' + file.n;
        console.log("newFilePath: " + newFilePath);

        if (fs.existsSync(newFilePath)) {
            var stats = fs.statSync(newFilePath);
            var fileSizeInBytes = stats.size;
            //Convert the file size to megabytes (optional)
            var fileSizeInMegabytes = fileSizeInBytes / 1000000.0;
            if (size <= fileSizeInMegabytes){
                console.log("fileSizeInMegabytes: " + fileSizeInMegabytes);
                console.log("RESOLVE: filesize big enough, resolving.");
                return resolve("RESOLVE: filesize big enough, resolving.");
            }
        }

        gCloudberryCam.getMedia(directory.d, file.n, newFilePath)
            .then(function (filename) {
                // Turn the camera on
                console.log("***   file has been saved ***");
                console.log(filename, '[saved]');
                console.log("RESOLVE: file has been saved.");
                return resolve("RESOLVE: file has been saved.");
            })
            .catch(function(fromReject){
                console.log('ERROR: getMedia caught a failure' + fromReject);
                return reject(fromReject);
            });
    });
    return promise
};

console.log("Download and delete the images from GoPro");
powerOn()
.then(function (resolveReturned) {
    console.log('powerOn: ' + resolveReturned);
    console.log("Now listing media...");
    gCloudberryCam.listMedia().then(function (result) {
        /*
        **  For each directory the camera has
        **  I haven't seen more than one
        */
        console.log("back from listMedia with result:");
        console.log(result);
        result.media.forEach(function (directory) {
            console.log('[directory] =', directory.d);
            console.log(directory);
            console.log(directory.fs);
            console.log(directory.fs.length);
            /*
            **  For each file in this directory
            */
            directory.fs.forEach(function (file) {
                return getImageFilename(directory, file).then(function(resolveReturned) {
                            console.log('getImageFilename resolved: ' + resolveReturned);
                            console.log("THE END.");
                            // return
                        }).catch(function(fromReject){
                            console.log('We have been rejected: getImageFilename ' + fromReject);
                            console.log('hurts, doesnt it?...');
                            // return;
                        });

                //totalDownloadSize = totalDownloadSize + size;
                // newFilePath = shutterBoxPath + '/'  + dateTakenClean + '-' + name;
                // console.log(newFilePath);
                // cam.getMedia(directory.d, file.n, newFilePath).then(function (filename) {

                //     console.log(filename, '[saved]');
                //     //console.log(totalDownloadSize, ' -- totalDownloadSize');
                //     // Now delete what you just dowloaded
                //     // cam.deleteLast().then(function () {
                //     //     console.log('[last media deleted]');
                //     // });
                // });
               //console.log('[url] = ', 'http://' + cam._ip + '/videos/DCIM/' + directory.d + '/' + file.n);
            });


            // function filename(e) {
            //   return new Promise(function(resolve, reject) {
            //     setTimeout(function(){ resolve(e), e * 1000});
            //   });
            // }

           // var arr = [1, 2, 3];
           //  var final = [];

           //  function download_all(arr) {

           //    return arr.reduce(function (promise, item) {
           //    // return directory.fs.reduce(function (promise, item) {
           //      return promise
           //        .then(function(result) {
           //          console.log('item ${item}');
           //          return filename(item).then(function(result) { final.push(result)});
           //        })
           //        .catch(console.error);
           //    }, Promise.resolve());
           //  }

           //  download_all(arr)
           //    .then(function(){ console.log('FINAL RESULT is ${final}')});

        });
    });

})
.then(function(resolveReturned){
    console.log('listing media resolved: ' + resolveReturned);
    return powerOff();
}).then(function(resolveReturned) {
    console.log('powerOff resolved: ' + resolveReturned);
    console.log("THE END.");
    return
}).catch(function(fromReject){
    console.log('We have been rejected: ' + fromReject);
    console.log('hurts, doesnt it?...');
    return;
});



// function filename(e) {
//   return new Promise((resolve, reject) => {
//     setTimeout(() => resolve(e), e * 1000);
//   });
// }

// const arr = [1, 2, 3];
// let final = [];

// function download_all(arr) {
//   return arr.reduce((promise, item) => {
//     return promise
//       .then((result) => {
//         console.log(`item ${item}`);
//         return filename(item).then(result => final.push(result));
//       })
//       .catch(console.error);
//   }, Promise.resolve());
// }

// download_all(arr)
//   .then(() => console.log(`FINAL RESULT is ${final}`));
