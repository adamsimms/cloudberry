// Zip. upload and the delete the contents of ShutterBox
// Angela Gabereau
// Sun Aug 6 2017 00:33 NFLD STD
// @ Studeerochee MTL

// Prerequiste: AWS installed, key configured
// Actions:
// - Zips up contents of ShutterBox
// - Uploads to AWS
// - Confirms successful upload to AWS
// - Deletes zip
// - Deletes content of ShutterBox
// 
// 


// var zipFolder = require('zip-folder');
 
// zipFolder('/path/to/the/folder', '/path/to/archive.zip', function(err) {
//     if(err) {
//         console.log('oh no!', err);
//     } else {
//         console.log('EXCELLENT');
//     }
// });

// 
// 
//  function getFileSize(filePath) {
//   var stats = fs.statSync(filePath);
//   // console.log('stats', stats);
//   var size = stats["size"];
//   // convert it to humanly readable format.
//   var i = Math.floor( Math.log(size) / Math.log(1024) );
//   return ( size / Math.pow(1024, i) ).toFixed(2) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
// }


// ///////
// const mkdirpAsync = function (dirPath) {
//   const fs = require('fs')
//   const path = require('path')

//   const mkdirAsync = currentPath => new Promise((resolve, reject) => {
//     fs.mkdir(currentPath, err => err ? reject(err) : resolve())
//   }).catch(err => {
//     if (err.code === 'EEXIST') return Promise.resolve()
//     throw err
//   })

//   let parts = dirPath.split(path.sep)
  
//   // Support absolute urls
//   if (parts[0] === '') {
//     parts.shift()
//     parts[0] = path.sep + parts[0]
//   }

//   let chain = Promise.resolve()

//   parts.forEach((part, i) => {
//     const currentPath = parts.slice(0, i + 1).join(path.sep)
//     chain = chain.then(() => mkdirAsync(currentPath))
//   })

//   return chain
// }

// // Example
// mkdirpAsync('a/b/c')
//   .then(() => console.log('Done!'))
//   .catch(err => console.error(err))

// ///////
// ///

// var mkdirp = require('mkdirp');
    
// mkdirp('/tmp/foo/bar/baz', function (err) {
//     if (err) console.error(err)
//     else console.log('pow!')
// });

/////////////