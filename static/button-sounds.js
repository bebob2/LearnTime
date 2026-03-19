document.addEventListener("DOMContentLoaded", function() {
    const addButtons = document.querySelectorAll(".button-add-sfx");
    const popButtons = document.querySelectorAll(".button-pop-sfx");
    const addSoundSrc = "/static/sounds/add_sfx.mp3";
    const popSoundSrc = "/static/sounds/pop_sfx.mp3";

    // Global volume control (0 - 1)
    const soundVolume = 0.6;

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const soundBuffers = { add: null, pop: null };

    const disableFormInputs = (form) => {
        if (!form) return;

        // Prevent changes while sound plays, but keep values submit-able.
        Array.from(form.elements).forEach((el) => {
            if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
                // Keep values included in submit; make readonly instead of disabled.
                el.readOnly = true;
            }

            // Disable submit buttons to prevent extra clicks.
            if (el.type === "submit" || el.type === "button") {
                el.disabled = true;
            }
        });
    };

    const loadSoundBuffer = async (url) => {
        const resp = await fetch(url);
        const arrayBuffer = await resp.arrayBuffer();
        return audioCtx.decodeAudioData(arrayBuffer);
    };

    const playBuffer = (buffer, gain = 1.0) => {
        const source = audioCtx.createBufferSource();
        source.buffer = buffer;

        const gainNode = audioCtx.createGain();
        gainNode.gain.value = gain;

        source.connect(gainNode).connect(audioCtx.destination);
        source.start();

        // Return a promise that resolves when playback ends.
        return new Promise((resolve) => {
            source.onended = resolve;
        });
    };

    // Preload sounds
    loadSoundBuffer(addSoundSrc)
        .then((buffer) => {
            soundBuffers.add = buffer;
        })
        .catch(() => {
            /* fallback: browser will play <audio> if decoding fails */
        });

    loadSoundBuffer(popSoundSrc)
        .then((buffer) => {
            soundBuffers.pop = buffer;
        })
        .catch(() => {
            /* fallback */
        });

    const playSound = (type) => {
        // Prefer WebAudio playback when possible (allows gain > 1)
        const buffer = soundBuffers[type];
        if (buffer) {
            // Make delete sound louder because its source is quieter.
            // WebAudio allows gain > 1.0 to amplify playback.
            const gain = type === "pop" ? 1.5 : soundVolume;
            return playBuffer(buffer, gain);
        }

        // Fallback to simple Audio element
        const audio = new Audio(type === "pop" ? popSoundSrc : addSoundSrc);
        audio.preload = "auto";
        audio.volume = soundVolume;
        return audio.play();
    };

    const submitAfterSound = (button, soundSrc) => {
        button.addEventListener("click", function(event) {
            // If this button should show a confirmation dialog (e.g. delete), do that first.
            if (button.classList.contains("confirm-delete") && !window.confirm("Are you sure you want to delete this item?")) {
                // Prevent form submission if the user cancels
                event.preventDefault();
                return;
            }

            const form = button.closest("form");
            if (form) {
                // If the form is invalid (e.g. required fields empty), allow
                // browser validation UI and do not submit.
                if (!form.checkValidity()) {
                    form.reportValidity();
                    return;
                }

                event.preventDefault();

                // Prevent the user from editing the form while the sound plays.
                disableFormInputs(form);
            }

            const playPromise = playSound(soundSrc === addSoundSrc ? "add" : "pop");

            const submitForm = () => {
                if (form && !form.dataset.soundSubmitted) {
                    form.dataset.soundSubmitted = "1";
                    form.submit();
                }
            };

            // If play() returns a promise, wait a short moment so the sound can be heard.
            if (playPromise && typeof playPromise.then === "function") {
                playPromise
                    .catch(() => {
                        /* ignore play errors */
                    })
                    .finally(() => setTimeout(submitForm, 150));
            } else {
                setTimeout(submitForm, 150);
            }
        });
    };

    addButtons.forEach(button => submitAfterSound(button, addSoundSrc));
    popButtons.forEach(button => submitAfterSound(button, popSoundSrc));

});

// this sctipt was created with the help of the chat extention copilot chat
