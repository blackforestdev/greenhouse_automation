// static/js/motorStatusHandler.js
import { MOTOR_IDS } from './config.js';

var socket = io.connect(`${window.location.protocol}//${window.location.hostname}:${window.location.port}`);

socket.on('connect', function() {
    console.log('Connected to WebSocket server');
});

socket.on('motor_status_updated', function(data) {
    console.log('Motor Status Update Received:', data);

    // Update the UI based on the received data
    var statusElement = document.getElementById(MOTOR_IDS[data.motor_switch_id] + '-status');
    if (statusElement) {
        statusElement.textContent = data.status;
    }

    var switchElement = document.getElementById(MOTOR_IDS[data.motor_switch_id] + '-switch');
    if (switchElement) {
        switchElement.checked = (data.status === 'Active'); // Update the checkbox based on the motor status
    }
});
