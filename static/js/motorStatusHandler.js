// static/js/motorStatusHandler.js

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('motor_status_updated', function(data) {
    console.log('Motor Status Update Received:', data);
    // Update the UI based on the received data
    var statusElement = document.getElementById('status_label_' + data.motor_switch_id);
    if (statusElement) {
        statusElement.textContent = data.status;
    }
});
