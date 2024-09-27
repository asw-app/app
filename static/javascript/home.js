document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0].replaceAll('-','/');
    document.getElementById("date").innerHTML = today;
});