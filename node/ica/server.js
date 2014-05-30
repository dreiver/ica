var debug	= true
var port 	= 3000//Listen port
var port_m	= 6380//Master port for redis
var http 	= require('http')
var redis	= require("redis")
var server 	= http.createServer()
var io 		= require('socket.io').listen(server)
var r 		= redis.createClient(port_m)//Client redis
var logs	= redis.createClient(port_m)//Client redis for ica:logs
var elogs	= redis.createClient(port_m)//Client redis for expired events in ica:logs
var admin 	= redis.createClient(port_m)//Client redis for ica:admin
var trunk	= redis.createClient(port_m)//Client redis for ica:trunk


//Listen to the server port
server.listen(port)


//JSON object for index channel
var index = {}
set_main();


//Handle clients
io.sockets.on('connection', function (client) {

	var r1 = redis.createClient(port_m); //Client redis for each user connected

	client.on("channel", function (channel) {
		r1.subscribe(channel);
	});

	r1.on("message", function (channel, message) {
		client.emit(channel, JSON.parse(message));
	});

	client.on('disconnect', function() {
		r1.end();
	});
});


//Listen to messages from ica:logs:* channel
logs.psubscribe('ica:logs:*');
logs.on("pmessage", function (pattern, channel, message) {
	var string = message
	var chann  = channel

	if (channel == "ica:logs:calls") {
		var object = JSON.parse(message)
		string 	   = JSON.stringify(object)

		r.publish("currentcalls", JSON.stringify(object));

		if (object['extension'] == "h")
			chann = remove_hangup(channel, object);
		else
			r.publish("index-graph", JSON.stringify(object));
	}
	
	r.lpush(chann, string);
	//r.expire(chann, '604800');
	r.llen(channel, function (err, len) {
		index[channel] = len;
		r.publish("index", JSON.stringify(index));
	});
});


//Listen to messages from ica:admin channel
admin.subscribe('ica:admin');
admin.on("message", function (channel, message) {
	var object = JSON.parse(message);

	//Admin options to manipulate the client browser!
	try {
		io.sockets.emit("admin", JSON.parse(message))
	} catch(err) {
	 	console.log("Error: "+err)
	}

	if (object['action'] == "refresh"){
		set_main (function (err, val) {
			r.publish("index", JSON.stringify(index));
		});
	}
});


//Listen to messages from ica:trunks channel
trunk.subscribe('ica:trunks');
trunk.on("message", function (channel, message) {
	//Update trunks state for all currently browsers
	r.publish("currentcalls-percent", JSON.stringify("update"));
});


//Listen to messages from ica:logs channel
elogs.psubscribe('__keyspace*__:ica:logs:*');
elogs.on("pmessage", function (pattern, channel, message) {
	if (message == "expired"){
		set_main (function ( err, val ) {
			r.publish("index", JSON.stringify(index));
		});
	}
});


function set_main (callback) {
	callback = callback || function() { return true; };
	r.llen("ica:logs:error", function (err, len) { 
		index["ica:logs:error"] = len;
		r.llen("ica:logs:calls", function (err, len) {
			index["ica:logs:calls"] = len;
			r.llen("ica:logs:warning", function (err, len) {
				index["ica:logs:warning"] = len;
				r.llen("ica:logs:serv:jpos", function (err, len) {
					index["ica:logs:serv:jpos"] = len;
					callback(len);
				});
			});
		});
	});
}


function remove_hangup(channel, object){
	var date = new Date();
	object['extension'] = object['dnid'];
	r.lrem(channel, -1, JSON.stringify(object));
	return "ica:reports:calls:day:"+("0" + date.getDate()).slice(-2)+(("0"+(date.getMonth()+1)).slice(-2))+date.getFullYear();
}