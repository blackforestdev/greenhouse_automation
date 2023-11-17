// static/js/timeManager.js

export function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
}

export function formatTime12Hour(time) {
    // Logic to format the given time in 12-hour format.
    // Return the formatted time.
}
