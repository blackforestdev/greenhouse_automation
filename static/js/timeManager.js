// static/js/timeManager.js

export function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
}

export function formatTime12Hour(timeString) {
    const [hours, minutes, seconds] = timeString.split(':');
    const hour = parseInt(hours, 10);
    const suffix = hour >= 12 ? 'PM' : 'AM';
    const formattedHour = ((hour + 11) % 12 + 1);
    return `${formattedHour}:${minutes}:${seconds} ${suffix}`;
}
