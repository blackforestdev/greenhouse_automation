// timeManager.js
export function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });  // Will format as HH:MM:SS AM/PM
}
