// static/js/main.js

import { MOTOR_IDS, MOTOR_STATUS_IDS } from './config.js';

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function toggleMotor(motorId, status) {
    fetch(`/motor_status/${motorId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: status ? 'Active' : 'Deactivated' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(`${status ? 'Activated' : 'Deactivated'} action successful for ${motorId}`);
            socket.emit('change_motor_status', { motorId: motorId, status: status });
        } else {
            console.error(`${status ? 'Activated' : 'Deactivated'} action failed for ${motorId}: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

socket.on('motor_status_updated', function(data) {
    // Update the UI based on the new motor status
    updateMotorStatusUI(data.motor_switch_id, data.status);
    updateCurrentStatus(data.status);
});

function updateMotorStatusUI(motorId, status) {
    // Logic to change the motor switch UI based on the received status
    var motorSwitch = document.getElementById(MOTOR_IDS[motorId] + '-switch');
    var statusElem = document.getElementById(MOTOR_STATUS_IDS[motorId]);
    if (motorSwitch && statusElem) {
        motorSwitch.checked = status === 'Active';
        statusElem.textContent = status;
    }
}

function updateCurrentStatus(action) {
    var currentStatus = document.getElementById('current-status');
    if (currentStatus) {
        switch (action) {
            case 'roll_up':
                currentStatus.textContent = 'All Motors rolling up';
                break;
            case 'roll_down':
                currentStatus.textContent = 'All Motors rolling down';
                break;
            case 'stop':
                currentStatus.textContent = 'All motors stopped';
                break;
            default:
                currentStatus.textContent = 'Motors idle';
                break;
        }
    }
}

Object.keys(MOTOR_IDS).forEach(motorId => {
    const motorSwitch = document.getElementById(MOTOR_IDS[motorId] + '-switch');
    if (motorSwitch) {
        motorSwitch.addEventListener('change', function() {
            toggleMotor(motorId, this.checked);
        });
    }
});

// Handle motor control buttons
document.querySelectorAll('.motor-control-btn').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.getAttribute('data-action');
        const motorId = this.getAttribute('data-motor-id') || 'all';

        fetch(`/motor_action/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ motor_id: motorId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log(`${action} action successful`);
                updateCurrentStatus(action);
            } else {
                console.error(`${action} action failed: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
