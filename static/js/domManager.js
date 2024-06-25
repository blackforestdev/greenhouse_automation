// static/js/domManager.js

import { getCurrentTime, formatTime12Hour } from './timeManager.js';
import { MOTOR_IDS, MOTOR_STATUS_IDS } from './config.js';

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
    motorId = motorId || 'all';
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
            const motorId = button.dataset.motorId || 'all';
            console.log(`Button clicked: ${action}`);
            triggerMotor(motorId, action);
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

    Object.keys(MOTOR_IDS).forEach(key => {
        const motor = { id: MOTOR_IDS[key], statusElem: MOTOR_STATUS_IDS[key] };
        console.log(`Checking motor switch with ID: ${motor.id}`);
        
        const switchElem = document.getElementById(motor.id);
        if (!switchElem) {
            console.error(`Switch element not found for ID: ${motor.id}`);
            return; 
        }
        
        console.log(`Found switch element for ID: ${motor.id}`);
        switchElem.addEventListener('change', (event) => {
            const status = event.target.checked ? 'Active' : 'Deactivated';
            updateMotorStatus(motor.id, status);

            const statusElem = document.getElementById(motor.statusElem);
            if (statusElem) {
                statusElem.textContent = status;
            } else {
                console.error(`Status element not found for ID: ${motor.statusElem}`);
            }
        });
    });
}

function updateMotorStatus(motorId, status) {
    const data = { status };
    console.log(`Sending request to update motor status: ${JSON.stringify(data)}`);

    fetch(`/motor_status/${motorId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(`Motor status updated: ${JSON.stringify(data)}`);
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
        const switchElemId = MOTOR_IDS[motor.motor_id];
        const switchElem = document.getElementById(switchElemId);
        const statusElem = document.getElementById(`${switchElemId}-status`);
        if (switchElem && statusElem) {
            switchElem.checked = motor.status === 'Active';
            statusElem.textContent = motor.status;
        }
    });
}

export function handleSetTimeForm() {
    const setTimeForm = document.getElementById('set-time-form');
    setTimeForm.addEventListener('submit', event => {
        event.preventDefault();
        const rollUpTime = document.getElementById('roll_up_time').value;
        const rollDownTime = document.getElementById('roll_down_time').value;
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
        if (data.status === 'success') {
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
        case 'stop':
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
    setTimeout(initMotorSwitches, 1000);  // Adding a delay to ensure the DOM is fully loaded
    motorControlButtonListener();
    fetchMotorStatuses();
    handleSetTimeForm();
    fetchSensorData();

    socket.on('motor_status_updated', data => {
        updateMotorSwitchesUI([data]);
        updateCurrentStatus(data.status);
    });

    socket.on('motor_action_response', data => {
        updateCurrentStatus(data.action);
    });

    socket.on('sensor_data_response', data => {
        updateSensorDataUI(data);
    });

    socket.on('current_times', data => {
        document.querySelector('#roll-up-time').textContent = formatTime12Hour(data.roll_up);
        document.querySelector('#roll-down-time').textContent = formatTime12Hour(data.roll_down);
    });
});
