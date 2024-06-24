// Main JS
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function toggleMotor(motorId, status) {
    fetch(`/motor_status/${motorId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: status ? 'Active' : 'Inactive' })
    })
    .then(response => {
        if (response.ok) {
            console.log(`${status ? 'Activated' : 'Deactivated'} action successful for ${motorId}`);
            socket.emit('change_motor_status', { motorId: motorId, status: status });
        } else {
            console.error(`${status ? 'Activated' : 'Deactivated'} action failed for ${motorId}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

socket.on('update_motor_status', function(data) {
    // Update the UI based on the new motor status
    updateMotorStatusUI(data.motorId, data.status);
    updateCurrentStatus(data.status);
});

function updateMotorStatusUI(motorId, status) {
    // Logic to change the motor switch UI based on the received status
    var motorSwitch = document.getElementById(motorId);
    if (motorSwitch) {
        motorSwitch.checked = status === 'Active';  // Assuming status is 'Active' or 'Inactive'
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

const motorIds = ['sidewall-left-switch', 'sidewall-right-switch', 'overhead-left-switch', 'overhead-right-switch'];
motorIds.forEach(motorId => {
    const motorSwitch = document.getElementById(motorId);
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
        fetch(`/motor_action/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                console.log(`${action} action successful`);
                updateCurrentStatus(action);
            } else {
                console.error(`${action} action failed`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
