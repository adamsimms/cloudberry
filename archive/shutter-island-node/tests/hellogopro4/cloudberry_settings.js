var GoPro = require('goproh4');

var cam = new GoPro.Camera();
let promise = new Promise(function(resolve, reject){
	// cleaning the room
	let isClean = true;

	if(!isClean){
		resolve('is clean');
	} else {
		reject('not');
	}
});
promise.then(function(fromResolve){
	console.log('the room is' + fromResolve);
	return;
}).catch(function(fromReject){
	console.log('the room is' + fromReject);
	return;
});

let cleanRoom = function(){
	console.log("cleanRoom");
	return new Promise(function(resolve, reject) {
		resolve("Cleaned the room");
	});
};
let removeGarbage = function(){
	console.log("removeGarbage");
	return new Promise(function(resolve, reject) {
		resolve("Took out garbage");
	});
};
let eatIcecream = function(){
	console.log("eatIcecream");
	return new Promise(function(resolve, reject) {
		resolve("Eat some ice cream");
	});
};

cleanRoom().then(function(resolveReturned){
	console.log(resolveReturned);
	return removeGarbage();
}).then(function(resolveReturned) {
	console.log(resolveReturned);
	return eatIcecream();
}).then(function(resolveReturned) {
	console.log(resolveReturned);
});

/*
**  Set the settings
*/

// Photo White Balance:
// Native: http://10.5.5.9/gp/gpControl/setting/22/4
// GoPro.Settings.PHOTO_PROTUNE_WHITE_BALANCE = 22;
// GoPro.Settings.PhotoProtuneWhiteBalance = {
//     Auto: 0,
//     B3000K: 1,
//     B4000K: 5,
//     B4800K: 6,
//     B5500K: 2,
//     B6000K: 7,
//     B6500K: 3,
//     Native: 4
// };
console.log("Setting the cloudberry settings");
console.log("Photo White Balance: Native");
cam.set(GoPro.Settings.PHOTO_PROTUNE_WHITE_BALANCE, GoPro.Settings.PhotoProtuneWhiteBalance.Native)
.then(function () {
	// Photo Color:
	// Flat: http://10.5.5.9/gp/gpControl/setting/23/1
	// GoPro.Settings.PHOTO_PROTUNE_COLOR = 23;
	// GoPro.Settings.PhotoProtuneColor = {
	//     GoProColor: 0,
	//     Flat: 1
	// };
	console.log("Photo Color: Flat");
    return cam.set(GoPro.Settings.PHOTO_PROTUNE_COLOR, GoPro.Settings.PhotoProtuneColor.Flat);
})
.then(function () {
	// Photo ISO Limit:
	// 400: http://10.5.5.9/gp/gpControl/setting/24/1
	// GoPro.Settings.PHOTO_PROTUNE_ISO = 24;
	// GoPro.Settings.PhotoProtuneIso = {
	//     I800: 0,
	//     I400: 1,
	//     I200: 2,
	//     I100: 3
	// };
	console.log("Photo ISO Limit: 400");
    return cam.set(GoPro.Settings.PHOTO_PROTUNE_ISO, GoPro.Settings.PhotoProtuneIso.I400);
})
.then(function () {
	// Photo ISO Min:
	// 100: http://10.5.5.9/gp/gpControl/setting/75/3
	// GoPro.Settings.PHOTO_PROTUNE_ISO_MIN = 75;
	// GoPro.Settings.PhotoProtuneIsoMin = {
	//     Im800: 0,
	//     Im400: 1,
	//     Im200: 2,
	//     Im100: 3
	// };
	console.log("Photo ISO Min: 100");
    return cam.set(GoPro.Settings.PHOTO_PROTUNE_ISO_MIN, GoPro.Settings.PhotoProtuneIsoMin.Im100);
})
.then(function () {
	// Photo Sharpness:
	// Med: http://10.5.5.9/gp/gpControl/setting/25/1
	// GoPro.Settings.PHOTO_PROTUNE_SHARPNESS = 25;
	// GoPro.Settings.PhotoProtuneSharpness = {
	//     High: 0,
	//     Medium: 1,
	//     Low: 2
	// };
	console.log("Photo Sharpness: Med");
    return cam.set(GoPro.Settings.PHOTO_PROTUNE_SHARPNESS, GoPro.Settings.PhotoProtuneSharpness.Medium);
})
.then(function () {
	// Photo resolution for Photo Modes (incl. SubModes):
	// 12MP Wide: http://10.5.5.9/gp/gpControl/setting/17/0
	// GoPro.Settings.PHOTO_RESOLUTION = 17;
	// GoPro.Settings.PhotoResolution = {
	//     R12MPWide: 0,
	//     R7MPWide: 1,
	//     R7MPMedium: 2,
	//     R5MPMedium: 3,
	//     //HERO5:
	//     R12MPLinear: 10,
	//     R12MPMedium: 8,
	//     R12MPNarrow: 9
	// };
	console.log("Photo resolution: 12MP Wide");
    return cam.set(GoPro.Settings.PHOTO_RESOLUTION, GoPro.Settings.PhotoResolution.R12MPWide);
})
.then(function () {
	// Photo Spot Meter:
	// off: http://10.5.5.9/gp/gpControl/setting/20/0
	// GoPro.Settings.PHOTO_SPOT_METER = 20;
	// GoPro.Settings.PhotoSpotMeter = {
	//     ON: 1,
	//     OFF: 0
	// };
	console.log("");
    return cam.set(GoPro.Settings.PHOTO_SPOT_METER, GoPro.Settings.PhotoSpotMeter.OFF);
});












