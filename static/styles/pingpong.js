var socket = io.connect('http://' + document.domain + ':' + location.port);

// 클라이언트가 ping 이벤트를 받으면 pong 이벤트로 응답
socket.on('ping', function() {
    socket.emit('pong');
});