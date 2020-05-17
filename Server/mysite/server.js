var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

app.get('/', function (req, res) {
  res.send('Hello World!');
});

// io.on('connection', function (socket) {
//   socket.on('chat message', function (msg) {
//     console.log('message: ' + msg);
//   });
// });

http.listen(9443, '113.161.56.123', function () {
  console.log('listening on *:20019');
});

io.on('connection', function (socket) {
  console.log('A client sent us this dumb message:');
  socket.emit('announcements', { message: 'A new user has joined!' });
  socket.on('event', function (data) {
    console.log('A client sent us this dumb message:', data.message);
  });
});
