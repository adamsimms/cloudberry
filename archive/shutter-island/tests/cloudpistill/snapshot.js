const Raspistill = require('node-raspistill').Raspistill;
const camera = new Raspistill();
//const camera = new Raspistill({outputDir:'/home/pi/spipi/photos', fileName: 'snapsnap'});
console.log("Gotta start somewhere");
camera.takePhoto().then((photo) => { console.log(photo); });
