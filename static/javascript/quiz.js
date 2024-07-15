// timer for quiz;
document.addEventListener('DOMContentLoaded', function()
{
    // set the duration of the timer
    var duration = 5 * 60; // 5 minutes in seconds

    // display the initial timer
    displayTime(duration); 

    var timer = duration, minutes, seconds;
    setInterval(function() {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById("timer").textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(timer);
            document.getElementById('quiz-form').submit();
        }
    }, 1000);

    function displayTime(seconds) {
        var minutes = Math.floor(seconds/60);
        var remainingSeconds = seconds % 60;
        document.getElementById('timer').textContent = 
            (minutes < 10 ? "0" : "") + minutes + ":" +
            (remainingSeconds < 10 ? "0" : "") + remainingSeconds;
    }
});