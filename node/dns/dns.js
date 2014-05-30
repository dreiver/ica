var redis  = require('redis'),
dnsd       = require('dnsd'),
nconf      = require('nconf'),
dns        = require('native-dns'),
util       = require('util'),
suffix     = 'dns_',
admin      = redis.createClient(),
dnsInterface, dnsPort, dnsZone, dnsMaster, r;

set_main();

function handler(req, res) {

  var question = res.question[0],
    hostname = question.name,
    length = hostname.length,
    ttl = Math.floor(Math.random() * 3600);

  var answer = {};

  if(question.type == 'A') {
    r.get(suffix+question.type+"_"+hostname, function(r_err, r_res) {

      if(r_err) {
        console.log('Redis error: '+r_err);
      } else {
        if(r_res !== null && r_res.length > 0) {

          answer = {
            name:hostname, 
            type:question.type,
            data:r_res, 
            'ttl':ttl};

          res.answer.push(answer);
          res.end()

          console.log('%s:%s/%s question:%j answer:%j', req.connection.remoteAddress, req.connection.remotePort, req.connection.type, question, answer);
        } else {
          /* No match in Redis, try to lookup in master server */
          var nativeQuestion = dns.Question({
            name: question.name,
            type: question.type
          });

          var start  = Date.now();
          var dns_master_server = dnsMaster;

          var nativeReq = dns.Request({
            question: nativeQuestion,
            server: { address: dns_master_server, port: 53, type: 'udp' },
            timeout: 1000
          });

          nativeReq.on('timeout', function () {
            console.log('native-dns: Timeout in making request');
          });

          nativeReq.on('message', function (err, answer) {
            answer.answer.forEach(function (a) {

              answer = {
                name:hostname,
                type:question.type,
                data:a.address,
                'ttl':ttl};

              res.answer.push(answer);
            });
          });

          nativeReq.on('end', function () {
            var delta = (Date.now()) - start;
            console.log('Finished processing request: ' + delta.toString() + 'ms');

            console.log('%s:%s/%s question:%j answer:%j', req.connection.remoteAddress, req.connection.remotePort, req.connection.type, question, res.answer);
            res.end();

          });
          nativeReq.send();
        }
      }
    }.bind(this));
  } else {
    res.end()
  }
  // redis error management
  r.on("error", function (err) {
    console.log("Redis error: " + err);
  });

}


function set_main (callback) {
  nconf.use('file', { file: __dirname + '/config.json' });
  nconf.load();

  dnsInterface = nconf.get('dns_interface');
  dnsPort      = nconf.get('dns_port');
  dnsZone      = nconf.get('dns_zone');
  dnsMaster    = nconf.get('dns_master');
  r            = redis.createClient();
}

var server = dnsd.createServer(handler);

server.zone(dnsZone, 'ns1.'+dnsZone, 'us@'+dnsZone, 'now', '2h', '30m', '2w', '10m')
  .listen(dnsPort, dnsInterface);
console.log('Server running at '+dnsInterface+':'+dnsPort);


// handle reload message with redis pub/sub
admin.subscribe('admin_dns');
admin.on("message", function (channel, message) {
  if (message == "reload") {
    console.log("reload message executed");
    set_main();
  }

  if (message == "restart") {
    console.log("restart message executed");
    process.exit(0);
  }
});


// redis error management
r.on("error", function (err) {
  console.log("Redis error: " + err);
});