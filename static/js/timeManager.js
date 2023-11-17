// static/js/timeManager.js

export function formatTime12Hour(time) {
    const date = new Date(`1970-01-01T${time}Z`);  // Create a Date object with the provided time
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
}
