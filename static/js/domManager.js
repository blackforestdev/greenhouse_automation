// static/js/domManager.js

import { getCurrentTime, formatTime12Hour } from './timeManager.js';

const socket = io();

export function updateCurrentTimeElement() {
    const currentTimeElement = document.querySelector('#current-time');
    currentTimeElement.textContent = getCurrentTime();
}

export function initTimeUpdater() {
    updateCurrentTimeElement();
    setInterval(updateCurrentTimeElement, 1000);
}

function triggerMotor(motorId, action) {
    // Ensure motorId and action are valid
    if (!motorId || !action) {
        console.error(`Invalid motorId (${motorId}) or action (${action})`);
        return;
    }

    const motorActionUrl = `/motor_action/${action}`;

    fetch(motorActionUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ motor_id: motorId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(`Motor ${motorId} ${action} successfully.`);
            updateCurrentStatus(action);
        } else {
            console.error(`Failed to ${action} motor ${motorId}: ${data.message}`);
        }
    })
    .catch(error => {
        console.error(`Error triggering motor ${motorId} ${action}:`, error);
    });
}

function motorControlButtonListener() {
    document.querySelectorAll('.motor-control-btn').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            console.log(`Button clicked: ${action}`);
            triggerMotor(null, action); // Assuming no specific motor ID for all motors action
        });
    });
}

export function requestTimes() {
    socket.emit('request_current_times');
}

socket.on('current_times', data => {
    console.log("Received time data:", data);

    const formattedRollUpTime = data.roll_up ? formatTime12Hour(data.roll_up) : "Not set";
    const formattedRollDownTime = data.roll_down ? formatTime12Hour(data.roll_down) : "Not set";

    console.log("Formatted Roll Up Time:", formattedRollUpTime);
    console.log("Formatted Roll Down Time:", formattedRollDownTime);

    document.getElementById('roll-up-time').textContent = formattedRollUpTime;
    document.getElementById('roll-down-time').textContent = formattedRollDownTime;
});

export function initMotorSwitches() {
    console.log("Initializing motor switches...");

    const motorSwitches = [
        { id: 'sidewall-left-switch', statusElem: 'sidewall-left-status' },
        { id: 'sidewall-right-switch', statusElem: 'sidewall-right-status' },
        { id: 'overhead-left-switch', statusElem: 'overhead-left-status' },
        { id: 'overhead-right-switch', statusElem: 'overhead-right-status' },
    ];

    motorSwitches.forEach(motor => {
        console.log(`Checking motor switch with ID: ${motor.id}`);
        
        const switchElem = document.getElementById(motor.id);
        if (!switchElem) {
            console.error(`Switch element not found for ID: ${motor.id}`);
            return; // Skip this iteration if the element is not found
        }
        
        console.log(`Found switch element for ID: ${motor.id}`);
        const status = switchElem.checked ? 'Active' : 'Deactivated';

        const statusElem = document.getElementById(motor.statusElem);
        if (statusElem) {
            statusElem.textContent = status;
        } else {
            console.error(`Status element not found for ID: ${motor.statusElem}`);
        }

        updateMotorStatus(motor.id, status);
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Received sensor data:", data);
        updateSensorDataUI(data);
    })
    .catch(error => {
        console.error('Error fetching sensor data:', error);
    });
}

function updateSensorDataUI(data) {
    document.getElementById('temperature').textContent = data.temperature ? `${data.temperature.toFixed(2)}°C` : "Not available";
    document.getElementById('humidity').textContent = data.humidity ? `${data.humidity.toFixed(2)}%` : "Not available";
    document.getElementById('vpd').textContent = data.vpd ? `${data.vpd.toFixed(2)} kPa` : "Not available";
}

function updateCurrentStatus(action) {
    const currentStatusElem = document.getElementById('current-status');
    switch (action) {
        case 'roll_up':
            currentStatusElem.textContent = 'All Motors rolling up';
            break;
        case 'roll_down':
            currentStatusElem.textContent = 'All Motors rolling down';
            break;
        case 'stop_motors':
            currentStatusElem.textContent = 'All motors stopped';
            break;
        default:
            currentStatusElem.textContent = 'Motors idle';
            break;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initTimeUpdater();
    requestTimes();
    initMotorSwitches();
    motorControlButtonListener();
    fetchMotorStatuses();
    handleSetTimeForm();
    fetchSensorData();

    // Listen for socket events to update current status
    socket.on('motor_status_updated', data => {
        updateCurrentStatus(data.status);
    });

    socket.on('motor_action_response', data => {
        updateCurrentStatus(data.action);
    });
});
