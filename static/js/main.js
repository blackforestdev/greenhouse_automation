// Main JS
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


function toggleMotor(motorId, status) {
    socket.emit('change_motor_status', {motorId: motorId, status: status});
}

socket.on('update_motor_status', function(data) {
    // Update the UI based on the new motor status
    updateMotorStatusUI(data.motorId, data.status);
});

function updateMotorStatusUI(motorId, status) {
    // Logic to change the motor switch UI based on the received status
    var motorSwitch = document.getElementById(motorId);
    if (motorSwitch) {
        motorSwitch.checked = status;  // Assuming status is a boolean
    }
}

var motorSwitch = document.getElementById('motorSwitchId');  // Replace 'motorSwitchId' with actual ID
motorSwitch.addEventListener('change', function() {
    toggleMotor('motorId', this.checked);  // Replace 'motorId' with actual motor ID
});

const motorIds = ['sidewall-left-switch', 'sidewall-right-switch', 'overhead-left-switch', 'overhead-right-switch'];
motorIds.forEach(motorId => {
    const motorSwitch = document.getElementById(motorId);
    if (motorSwitch) {
        motorSwitch.addEventListener('change', function() {
            toggleMotor(motorId, this.checked);
        });
    }
});
