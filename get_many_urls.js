// reads a lot of URLs concurrently and saves the results into a directory

// USAGE: node read_many_urls.js <url_csv_file> <output dir>
// url_csv_file should have a format of <id>, <url> - ID will be used for the file id inside the dir 

var fs		= require('fs');
var csv 	= require('csv');
// var http	= require('http');
var util	= require('util');
var request = require('request');


// var data = new Array();
var args = process.argv;
console.log(args);
// process.exit(0);

var url_csv_file = args[2];
var output_dir   = args[3];
console.log('url_csv_file: ' + url_csv_file + '\noutput_dir: ' + output_dir);

// process.exit(0);

csv()
.from.stream(fs.createReadStream(url_csv_file)) //  __dirname+'/locations.csv')
.on('record', function(record, index){
	id  = record[0];
	url = record[1];
	read_url(id, url);
});


function read_url(id, url) {
	console.log('reading ' + url);

	request(url, function (error, response, body) {
		if (!error && response.statusCode == 200) {
			fs.writeFileSync(output_dir+'/'+id, body);
		} else {
			console.log("Error: " + error + "when reading " + url);
		}
	});
}


// process.on('exit',	
// 	function () {
// 		// this is obviously not the clean way to do it, but new to Node,js, cut me some slack.
// 		out = "";
// 		for (i in data) {
// 			out += JSON.stringify(data[i]).replace("[","").replace("]","") + "\n";
// 		}
// 		fs.writeFileSync(__dirname+'/locations_with_coords.csv', out);
// 	}
// );


// Processing 1098 locations:
// localhost:israel_coordinates niryariv$ date; node parse.js ; date
// Sat Feb 23 15:33:19 IST 2013
// Got error: Error: socket hang up
// Sat Feb 23 15:37:25 IST 2013