Introduction
------------

A NodeJS DNS server that is configured using Redis. Names not found in redis are looked up into master DNS server.

Installation
------------

Pre-requisite:

 * NodeJs
 * Redis server

Make sure to setup DNS correctly on the hosts where you want to use this DNS server. Check /etc/resolv.conf if you're running on unix. In windows, check the network settings in the control panel.

Install: `npm install --production`

Update with your settings to `config.json`
Start the server: `node dns.js`


Test the setup
--------------

Start with setting up some hosts with their IP:s in redis (make sure redis is installed an running)

```
redis-cli set dns_A_redis-dns.local 10.0.0.1
redis-cli set dns_A_appserver.local 10.0.0.2
```

We can use `dig` for testing purposes.

`dig @localhost -p 5353 dbserver.redis-dns.local A`

`dig @localhost -p 5353 dbserver.redis-dns.local MX`

