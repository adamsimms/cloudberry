var params = {
    Bucket: config.get('s3bucket'),
    Key: path
};


s3.headObject(params, function (err, metadata) {  
  if (err && err.code === 'NotFound') {  
    // Handle no object on cloud here  
  } else {  
    s3.getSignedUrl('getObject', params, callback);  
  }
});

///////////


var s3 = require('aws2js').load('s3', process.env.AWS_ACCEESS_KEY_ID, process.env.AWS_SECRET_ACCESS_KEY)

s3.setBucket(process.env.AWS2JS_S3_BUCKET)

s3.head(process.argv[2], function (err, res) {
    if (err) {
        console.log(err)
        return
    }
    console.log(res)
})

////////

Promise = require 'bluebird'
AWS = require 'aws-sdk'
AWS.config.accessKeyId = Config.Credentials.AWS.accessKeyId
AWS.config.secretAccessKey = Config.Credentials.AWS.secretAccessKey

S3 = new AWS.S3
Promise.promisifyAll S3

S3.headObjectAsync
    Bucket: 'bucketname'
    Key: 'file.txt'
.then (result)->
    console.log 'success'
    console.log result # this is an metadata object for the file, as seen below:
    ###
    { AcceptRanges: 'bytes',
    LastModified: 'Mon, 16 Jan 2017 07:30:19 GMT',
    ContentLength: '6',
    ETag: '"b1946ac92492d2347c6235b4d2611184"',
    ContentType: 'text/plain',
    Metadata: {} }
    ###
.catch (error)->
    console.log 'failure'
    console.log error.statusCode # 404

    /////////////

    /* The following example retrieves an object metadata. */

 var params = {
  Bucket: "examplebucket", 
  Key: "HappyFace.jpg"
 };
 s3.headObject(params, function(err, data) {
   if (err) console.log(err, err.stack); // an error occurred
   else     console.log(data);           // successful response
   /*
   data = {
    AcceptRanges: "bytes", 
    ContentLength: 3191, 
    ContentType: "image/jpeg", 
    ETag: "\"6805f2cfc46c0f04559748bb039d69ae\"", 
    LastModified: <Date Representation>, 
    Metadata: {
    }, 
    VersionId: "null"
   }
   */
 });


 ////////

// var s3 = new AWS.S3();
// var params = {Bucket: 'mybucket', Key: 'myfile'};
// s3.getObject(params).on('success', function(response) {
//   console.log("Key was", response.request.params.Key);
// }).on('error',function(error){
//      //error return a object with status code 404
// }).send();

// var s3 = new AWS.S3();
// var params = {Bucket: 'mybucket', Key: 'myfile'};
// s3.headObject(params).on('success', function(response) {
//   console.log("Key was", response.request.params.Key);
// }).on('error',function(error){
//      //error return a object with status code 404
// }).send();