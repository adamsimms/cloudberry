var GoPro = require('goproh4'),
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
checkClouberryProSettings = function() {
	var promise = new Promise(function(resolve, reject){
		console.log('*** Checking the Cloudberry GoPro Settings ***');
		return gCloudberryCam.status()
		.then(function (status) {
			console.log('-- Photo White Balance: Native, 22/4 [setting.22] = ', status.settings[22]);
		    if (4 != status.settings[22]) { console.log("!! 22 ain't right"); }

		    console.log('-- Photo Color: Flat, 23/1 [setting.23] = ', status.settings[23]);
		    if (1 != status.settings[23]) { console.log("!! 23 ain't right"); }

		    console.log('-- Photo ISO Limit: 400, 24/1 [setting.24] = ', status.settings[24]);
		    if (1 != status.settings[24]) { console.log("!! 24 ain't right"); }

		    console.log('-- Photo ISO Min: 100, 75/3 [setting.75] = ', status.settings[75]);
		    if (3 != status.settings[75]) { console.log("!! 75 ain't right"); }

		    console.log('-- Photo Sharpness: Med, 25/1 [setting.25] = ', status.settings[25]);
		    if (1 != status.settings[25]) { console.log("!! 25 ain't right"); }

		    console.log('-- Photo resolution: 12MP Wide, 17/0 [setting.17] = ', status.settings[17]);
		    if (0 != status.settings[17]) { console.log("!! 17 ain't right"); }

		    console.log('-- Photo Spot Meter: off, 20/0 [setting.20] = ', status.settings[20]);
		    if (0 != status.settings[20]) { console.log("!! 20 ain't right"); }

		    return 'Done checking settings'
		})
		.then(function(){
			console.log("That is all.");
			resolve("checkClouberryProSettings resolves");
		})
		.catch(function(fromReject){
			console.log('ERROR: checkClouberryProSettings caught a failure' + fromReject);
			reject(fromReject);
		});

	});
	return promise;
},
settingClouberryProSettings = function() {
	var promise = new Promise(function(resolve, reject){
		/*
		**  Set the settings
		*/
		console.log("*** Setting the Cloudberry GoPro Settings ***");
		// Set camera mode
		return gCloudberryCam.mode(GoPro.Settings.Modes.Photo, GoPro.Settings.Submodes.Photo.Single)
		.then(function () {
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
			console.log("-- Photo White Balance: Native");
			return gCloudberryCam.set(GoPro.Settings.PHOTO_PROTUNE_WHITE_BALANCE, GoPro.Settings.PhotoProtuneWhiteBalance.Native)
		})
		.then(function () {
			// Photo Color:
			// Flat: http://10.5.5.9/gp/gpControl/setting/23/1
			// GoPro.Settings.PHOTO_PROTUNE_COLOR = 23;
			// GoPro.Settings.PhotoProtuneColor = {
			//     GoProColor: 0,
			//     Flat: 1
			// };
			console.log("-- Photo Color: Flat");
		    return gCloudberryCam.set(GoPro.Settings.PHOTO_PROTUNE_COLOR, GoPro.Settings.PhotoProtuneColor.Flat);
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
			console.log("-- Photo ISO Limit: 400");
		    return gCloudberryCam.set(GoPro.Settings.PHOTO_PROTUNE_ISO, GoPro.Settings.PhotoProtuneIso.I400);
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
			console.log("-- Photo ISO Min: 100");

			//console.log(GoPro.Settings);
			// Strangely, does not have this settings.  let's just hard code value. TODO: Wht not in settings??  
			// return gCloudberryCam.set(GoPro.Settings.PHOTO_PROTUNE_ISO_MIN, GoPro.Settings.PhotoProtuneIsoMin.Im100);
			return gCloudberryCam.set(75, 3);
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
			console.log("-- Photo Sharpness: Med");
		    return gCloudberryCam.set(GoPro.Settings.PHOTO_PROTUNE_SHARPNESS, GoPro.Settings.PhotoProtuneSharpness.Medium);
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
			console.log("-- Photo resolution: 12MP Wide");
		    return gCloudberryCam.set(GoPro.Settings.PHOTO_RESOLUTION, GoPro.Settings.PhotoResolution.R12MPWide);
		})
		.then(function () {
			// Photo Spot Meter:
			// off: http://10.5.5.9/gp/gpControl/setting/20/0
			// GoPro.Settings.PHOTO_SPOT_METER = 20;
			// GoPro.Settings.PhotoSpotMeter = {ss
			//     ON: 1,
			//     OFF: 0
			// };
			console.log("-- sPhoto Spot Meter: off");
		    return gCloudberryCam.set(GoPro.Settings.PHOTO_SPOT_METER, GoPro.Settings.PhotoSpotMeter.OFF);
		})
		.then(function(){
			console.log("That is all.");
			resolve("resolved settingClouberryProSettings");
		})
		.catch(function(fromReject){
			console.log('ERROR: settingClouberryProSettings caught a failure' + fromReject);
			reject(fromReject);
		});
	});
	return promise;
};

powerOn().then(function(resolveReturned){
	console.log('powerOn resolved: ' + resolveReturned);
	return checkClouberryProSettings();
}).then(function(resolveReturned){
	console.log('checkClouberryProSettings first time resolved: ' + resolveReturned);
	return settingClouberryProSettings();
}).then(function(resolveReturned) {
	console.log('settingClouberryProSettings resolved: ' + resolveReturned);
	return checkClouberryProSettings();
}).then(function(resolveReturned) {
	console.log('checkClouberryProSettingssecond time resolved: ' + resolveReturned);
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
