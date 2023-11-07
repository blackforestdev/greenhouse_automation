import { getCurrentTime } from './timeManager.js';

const socket = io();

export function updateCurrentTimeElement() {
    const currentTimeElement = document.querySelector('#current-time');
    currentTimeElement.textContent = getCurrentTime();
}

export function initTimeUpdater() {
    updateCurrentTimeElement();
    setInterval(updateCurrentTimeElement, 1000);
}

export function triggerMotor(action) {
    // Create an object to store the status of each motor switch
    let motorStatuses = {
        'motor_1': document.getElementById('sidewall-left-switch').checked,
        'motor_2': document.getElementById('sidewall-right-switch').checked,
        'motor_3': document.getElementById('overhead-left-switch').checked,
        'motor_4': document.getElementById('overhead-right-switch').checked
    };

    fetch(`/motor_action/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ motor_statuses: motorStatuses })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Alert with the action performed
        alert(`${action.replace('_', ' ')}: ${data.message}`);
    })
    .catch(error => {
        console.error('Fetch operation error:', error.message);
        alert('An error occurred.');
    });
}


function motorControlButtonListener() {
    document.querySelectorAll('.motor-control-btn').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            console.log("Button clicked:", action); //Added for testing
            // Trigger the action for all motors regardless of individual motor IDs
            triggerMotor(action);
        });
    });
}

export function requestTimes() {
    socket.emit('request_current_times');
}

socket.on('current_times', data => {
    document.getElementById('roll-up-time').textContent = data.roll_up || "Not set";
    document.getElementById('roll-down-time').textContent = data.roll_down || "Not set";
});

export function initMotorSwitches() {
    const motorSwitches = [
        { id: 'sidewall-left-switch', statusElem: 'sidewall-left-status' },
        { id: 'sidewall-right-switch', statusElem: 'sidewall-right-status' },
        { id: 'overhead-left-switch', statusElem: 'overhead-left-status' },
        { id: 'overhead-right-switch', statusElem: 'overhead-right-status' },
    ];

    motorSwitches.forEach(motor => {
        const switchElem = document.getElementById(motor.id);
        switchElem.addEventListener('change', () => {
            const status = switchElem.checked ? 'Active' : 'Deactivated';
            document.getElementById(motor.statusElem).textContent = status;
            updateMotorStatus(motor.id, status);
        });
    });
}

function updateMotorStatus(motorId, status) {
    fetch(`/motor_status/${motorId}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ status })
    })
    .catch(error => console.error('Error updating motor status:', error));
}

export function fetchMotorStatuses() {
    fetch('/get_motor_statuses')
    .then(response => response.json())
    .then(updateMotorSwitchesUI)
    .catch(error => console.error('Error fetching motor statuses:', error));
}

function updateMotorSwitchesUI(motorStatuses) {
    motorStatuses.forEach(motor => {
        let motorName = getMotorName(motor.motor_id);
        let switchElemId = `${motorName}-switch`;
        let switchElem = document.getElementById(switchElemId);
        let statusElem = document.getElementById(`${motorName}-status`);
        if (switchElem && statusElem) {
            switchElem.checked = motor.status === 'Active';
            statusElem.textContent = motor.status;
        }
    });
}

function getMotorName(motorId) {
    switch (motorId) {
        case 1: return 'sidewall-left';
        case 2: return 'sidewall-right';
        case 3: return 'overhead-left';
        case 4: return 'overhead-right';
        default: return 'unknown';
    }
}

export function handleSetTimeForm() {
    const setTimeForm = document.getElementById('set-time-form');
    setTimeForm.addEventListener('submit', event => {
        event.preventDefault();
        let rollUpTime = document.getElementById('roll_up_time').value;
        let rollDownTime = document.getElementById('roll_down_time').value;
        submitTimeSettings(rollUpTime, rollDownTime);
    });
}

function submitTimeSettings(rollUpTime, rollDownTime) {
    fetch('/set_time', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `roll_up_time=${encodeURIComponent(rollUpTime)}&roll_down_time=${encodeURIComponent(rollDownTime)}`
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success') {
            alert('Times set successfully!');
            requestTimes();
        } else {
            alert('Error setting times.');
        }
    })
    .catch(error => console.error('Error setting times:', error));
}

export function fetchSensorData() {
    fetch('/get_sensor_data')
    .then(response => response.json())
    .then(data => updateSensorDataUI(data))
    .catch(error => console.error('Error fetching sensor data:', error));
}

function updateSensorDataUI(data) {
    document.getElementById('temperature').textContent = data.temperature || "Not available";
    document.getElementById('humidity').textContent = data.humidity || "Not available";
    document.getElementById('vpd').textContent = data.vpd || "Not available";
}

document.addEventListener('DOMContentLoaded', () => {
    initTimeUpdater();
    requestTimes();
    initMotorSwitches();
    motorControlButtonListener();
    fetchMotorStatuses();
    handleSetTimeForm();
    fetchSensorData();
});