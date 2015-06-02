/* Node.js */
var Parse = require('parse').Parse;
var appId = "vQMTQvjGqlWYawkVGme21jeL7FQ3VEEeetu2Cg6R";
var jsKey = "n9QwHXBE6D1AOcSufvG370uWDgNJOvFScNEVH87w";

Parse.initialize(appId, jsKey);

function insert(objectName, data){
  var Obj = Parse.Object.extend(objectName);
  var obj = new Obj();
  obj.save(data, {
    success: function(obj){ process.exit(0); },
    error: function(obj, error){ process.exit(-1); }
   });
}

/* main function */

if (process.argv.length < 5){
  console.log("node Parse.js <method> <object_name> <data>");
  return;
}

var method = process.argv[2];
var objectName = process.argv[3];
var data = JSON.parse(process.argv[4]);

if (method == "insert"){
  insert(objectName, data);
}
