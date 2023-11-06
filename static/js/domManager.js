import { getCurrentTime } from './timeManager.js';

// Initialize the socket connection
const socket = io();

// Update the content of the #current-time element with the current time
export function updateCurrentTimeElement() {
    const currentTimeElement = document.querySelector('#current-time');
    currentTimeElement.textContent = getCurrentTime();
}

// Initialize time updating: set the current time immediately and then update every 1 second
export function initTimeUpdater() {
    updateCurrentTimeElement();  // Initial update
    setInterval(updateCurrentTimeElement, 1000);  // Update every 1 second
}

export function triggerMotor(action) {
    fetch(`/motor_action/${action}`, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(`${action.replace('_', ' ')} successfully triggered!`);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error.message);
        alert('An error occurred.');
    });
}

// Function to handle the motor control and stop motor button events
function motorControlButtonListener() {
    document.querySelectorAll('.motor-control-btn').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            if (action === 'stop_motors') {
                socket.emit('stop_motor');
            } else {
                triggerMotor(action);
            }
        });
    });
}

// Function to request roll up and down times from the server
export function requestTimes() {
    socket.emit('request_current_times');
}

// Event listeners for socket events
socket.on('current_times', (data) => {
    document.getElementById('roll-up-time').textContent = data.roll_up || "Not set";
    document.getElementById('roll-down-time').textContent = data.roll_down || "Not set";
});

socket.on('motor_action_result', (data) => {
    if (data.action && data.result) {
        alert(`${data.action.replace('_', ' ')} ${data.result}`);
    } else {
        alert('An error occurred with the motor action.');
    }
});

socket.on('stop_motor_result', (data) => {
    if (data.status === 'success') {
        alert('Motors stopped successfully!');
    } else {
        alert('Failed to stop motors.');
    }
});

// Switches to Activate or Deactivate each motor
export function initMotorSwitches() {
    const motorSwitches = [
        { id: 'sidewall-left-switch', statusElem: 'sidewall-left-status' },
        { id: 'sidewall-right-switch', statusElem: 'sidewall-right-status' },
        { id: 'overhead-left-switch', statusElem: 'overhead-left-status' },
        { id: 'overhead-right-switch', statusElem: 'overhead-right-status' },
    ];

    motorSwitches.forEach(motor => {
        const switchElem = document.getElementById(motor.id);
        switchElem.addEventListener('change', function() {
            const status = switchElem.checked ? 'Active' : 'Deactivated';
            document.getElementById(motor.statusElem).textContent = status;

            // Now, send the status to the server
            fetch(`/motor_status/${motor.id}`, {
                method: 'POST',
                body: JSON.stringify({ status: status }),
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error.message);
            });
        });
    });
}

export function fetchMotorStatuses() {
    fetch('/get_motor_statuses')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        data.forEach(motor => {
            let motorName;
            switch (motor.motor_id) {
                case 1: motorName = 'sidewall-left'; break;
                case 2: motorName = 'sidewall-right'; break;
                case 3: motorName = 'overhead-left'; break;
                case 4: motorName = 'overhead-right'; break;
            }

            const switchElemId = motorName + '-switch';
            const switchElem = document.getElementById(switchElemId);
            const statusElem = document.getElementById(motorName + '-status');
            if (switchElem && statusElem) {
                switchElem.checked = motor.status === 'Active';
                statusElem.textContent = motor.status;
            }
        });
    })
    .catch(error => {
        console.error('Error fetching motor statuses:', error);
        alert('Failed to fetch motor statuses.');
    });
}

// Function to handle the set time form submission
export function handleSetTimeForm() {
    const setTimeForm = document.getElementById('set-time-form');

    setTimeForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const rollUpTime = document.getElementById('roll_up_time').value;
        const rollDownTime = document.getElementById('roll_down_time').value;

        fetch('/set_time', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `roll_up_time=${encodeURIComponent(rollUpTime)}&roll_down_time=${encodeURIComponent(rollDownTime)}`
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                alert('Times set successfully!');
                requestTimes();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while setting times');
        });
    });
}

// Function to fetch sensor data from the Flask backend
export function fetchSensorData() {
    fetch('/get_sensor_data')
    .then(response => response.json())
    .then(data => {
        document.getElementById('temperature').textContent = data.temperature || "Not available";
        document.getElementById('humidity').textContent = data.humidity || "Not available";
        document.getElementById('vpd').textContent = data.vpd || "Not available";
    })
    .catch(error => console.error('Error fetching sensor data:', error));
}

// Initialize everything when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initTimeUpdater();
    requestTimes();
    initMotorSwitches();
    motorControlButtonListener();
    handleSetTimeForm();
    fetchSensorData();
});
