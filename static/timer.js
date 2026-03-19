// The following is created by the Google Ai to warn upon closing the page
function showWarning(e) {
    e.preventDefault();
    e.returnValue = ''; // Required for most modern browsers to show the prompt
}


// ------------------now the following is created by me exept sth. diffrent is specified


const defaultMinutes = 90;
let minutes = defaultMinutes;
let seconds = 0;

// Load minutes from LocalStorage (use strict null check so 0 is preserved)
if (localStorage.getItem('minutes') === null) {
    localStorage.setItem('minutes', minutes);
} else {
    minutes = parseInt(localStorage.getItem('minutes')) || 0;
}
// Load seconds from LocalStorage (use strict null check so 0 is preserved)
if (localStorage.getItem('seconds') === null) {
    localStorage.setItem('seconds', 0);
} else {
    seconds = parseInt(localStorage.getItem('seconds')) || 0;
}

let initial_minutes = minutes; // Store initial minutes for progress bar reset
let initial_seconds = seconds; // Store initial seconds for progress bar reset

const alarm_sound = new Audio('/static/sounds/alarm-sound-1.mp3');

document.addEventListener('DOMContentLoaded', () => {

    // get Elements by id
    const decButton = document.getElementById('decButton');
    const incButton = document.getElementById('incButton');
    const timerDisplay = document.getElementById('timer');
    const startButton = document.getElementById('startButton');
    const resetButton = document.getElementById('resetButton');
    const stopButton = document.getElementById('stopButton');
    const titleElement = document.getElementById('title');
    const progressBar = document.querySelector('progress');
    const subjectSelect = document.getElementById('subjectSelect');
    const presetButtons = document.querySelectorAll('.preset-btn');

     // Add click listeners to preset buttons (with copilot's help to save time)
     presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const presetMinutes = parseInt(button.value);
            if (!isNaN(presetMinutes)) {
                minutes = presetMinutes;
                seconds = 0;
                updateDisplay();
                saveState();
            }
        });
    });

    let subject_id = subjectSelect.value; // Initialize subject variable

    const defaultTitle = 'LearnTime: Home';

    const updateDisplay = () => {
        timerDisplay.innerHTML = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        if (timerInterval) {
            titleElement.innerHTML = `${minutes}:${seconds.toString().padStart(2, '0')} - LearnTime`;
        }
        else {
            progressBar.max = minutes; // Update progress bar max when changing time
        }
        progressBar.value = minutes + (seconds / 60); // Update progress bar value based on minutes and seconds
    };

    // Track interval so we can stop it later
    let timerInterval = null;

    // Ensure title is correct before timer starts
    titleElement.innerHTML = defaultTitle;

    const saveState = () => {
        localStorage.setItem('minutes', minutes);
        localStorage.setItem('seconds', seconds);
    };

    updateDisplay();

    decButton.addEventListener('click', () => {
        minutes = Math.max(0, minutes - 1);
        seconds = 0;
        updateDisplay();
        saveState();
    });

    incButton.addEventListener('click', () => {
        minutes++;
        seconds = 0;
        updateDisplay();
        saveState();
    });

    resetButton.addEventListener('click', () => {
        minutes = defaultMinutes;
        seconds = 0;
        updateDisplay();
        saveState();
    });

    startButton.addEventListener('click', () => {  // created with the help of copilot
        if (timerInterval) return; // already running

        startButton.disabled = true;
        stopButton.disabled = false;
        decButton.disabled = true;
        incButton.disabled = true;
        resetButton.disabled = true;
        subjectSelect.disabled = true;
        presetButtons.forEach(button => button.disabled = true); // Disable preset buttons when timer starts

        progressBar.max = minutes;
        progressBar.value = minutes;

        subject_id = subjectSelect.value; // Update subject variable when starting timer

        initial_minutes = minutes; // Update initial minutes
        initial_seconds = seconds; // Update initial seconds

        window.addEventListener('beforeunload', showWarning);

        timerInterval = setInterval(() => {
            if (seconds === 0) {
                if (minutes === 0) {
                    clearInterval(timerInterval);
                    timerInterval = null;

                    // ringing settings:
                    alarm_sound.currentTime = 0; // Reset to start in case it's still playing
                    alarm_sound.loop = true; // Loop the alarm sound until user stops it
                    alarm_sound.play();
                    titleElement.innerHTML = 'Time is up! - LearnTime';

                    return;
                }
                minutes--;
                seconds = 59;
            } else {
                seconds--;
            }
            updateDisplay();
            saveState();
        }, 1000);
    });

    stopButton.addEventListener('click', () => { // created with the help of copilot
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        else {
            alarm_sound.pause();
            alarm_sound.currentTime = 0; // Reset to start in case it's still playing
            titleElement.innerHTML = defaultTitle;
        }

        window.removeEventListener('beforeunload', showWarning);
        startButton.disabled = false;
        stopButton.disabled = true;
        decButton.disabled = false;
        incButton.disabled = false;
        resetButton.disabled = false;
        subjectSelect.disabled = false;
        presetButtons.forEach(button => button.disabled = false); // Re-enable preset buttons when timer stops

        titleElement.innerHTML = defaultTitle;

        // redirect to store learned time for the subject written with the help of copilot
        const learnedTime = initial_minutes - minutes + (initial_seconds - seconds) / 60; // Calculate learned time in minutes
        if (learnedTime > 0 && subject_id) {
            // Send POST request to server to store learned time for the subject
            fetch('/store_learned_time', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ subject_id: subject_id, learned_time: learnedTime })
            })
            .then(response => {
                const contentType = response.headers.get('content-type') || '';
                if (!response.ok) {
                    throw new Error(`Server responded with ${response.status}`);
                }
                if (contentType.includes('application/json')) {
                    return response.json();
                }
                return null;
            })
            .then(data => {
                if (data) {
                    console.log('Learned time stored successfully:', data);
                } else {
                    console.log('Learned time stored successfully (no JSON response).');
                }
            })
            .catch((error) => {
                console.error('Error storing learned time:', error);
            });
        }
    });

    const links = document.querySelectorAll('a');

    // Only allow navigation away without a warning if the timer is NOT running.
    // If the timer is running, we keep the beforeunload listener to prompt the user.
    links.forEach(link => {
        link.addEventListener('click', () => {
            if (!timerInterval) {
                window.removeEventListener('beforeunload', showWarning);
            }
        });
    });

});

