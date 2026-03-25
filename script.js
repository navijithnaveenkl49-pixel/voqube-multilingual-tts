const synth = window.speechSynthesis;

// DOM Elements
const textInput = document.getElementById('text-input');
const voiceSelect = document.getElementById('voice-select');
const speakBtn = document.getElementById('speak-btn');
const stopBtn = document.getElementById('stop-btn');
const rateInput = document.getElementById('rate');
const pitchInput = document.getElementById('pitch');
const rateValue = document.getElementById('rate-value');
const pitchValue = document.getElementById('pitch-value');
const visualizer = document.querySelector('.visualizer');
const charCount = document.querySelector('.char-count');

// State
let voices = [];
let isSpeaking = false;

// Indian Language Codes to Filter
const indianLangCodes = [
    'en-IN', // English (India)
    'hi-IN', // Hindi (India)
    'bn-IN', // Bengali (India)
    'ta-IN', // Tamil (India)
    'te-IN', // Telugu (India)
    'mr-IN', // Marathi (India)
    'gu-IN', // Gujarati (India)
    'kn-IN', // Kannada (India)
    'ml-IN', // Malayalam (India)
    'pa-IN'  // Punjabi (India)
];

// Initialize Voices
function getVoices() {
    voices = synth.getVoices().filter(voice => {
        // Strict filter for Indian languages OR loose check for "India" in name
        return indianLangCodes.includes(voice.lang) || voice.name.includes('India');
    });

    // Sort voices: Hindi/Indian English first if possible, then others
    voices.sort((a, b) => {
        const aName = a.name.toLowerCase();
        const bName = b.name.toLowerCase();
        if (aName.includes('hindi') && !bName.includes('hindi')) return -1;
        if (!aName.includes('hindi') && bName.includes('hindi')) return 1;
        return a.lang.localeCompare(b.lang);
    });

    voiceSelect.innerHTML = '';

    if (voices.length === 0) {
        const option = document.createElement('option');
        option.textContent = "NO INDIAN VOICES DETECTED (CHECK SYSTEM SETTINGS)";
        option.disabled = true;
        voiceSelect.appendChild(option);
    } else {
        voices.forEach(voice => {
            const option = document.createElement('option');
            option.textContent = `${voice.name} (${voice.lang})`;
            option.setAttribute('data-lang', voice.lang);
            option.setAttribute('data-name', voice.name);
            voiceSelect.appendChild(option);
        });
    }
}

// Event Listeners
if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = getVoices;
}
getVoices(); // Initial call

// Update Slider Values
rateInput.addEventListener('input', e => rateValue.textContent = e.target.value);
pitchInput.addEventListener('input', e => pitchValue.textContent = e.target.value);

// Text Input Character Count
textInput.addEventListener('input', () => {
    charCount.textContent = `${textInput.value.length} / 5000`;
    if (textInput.value.length > 5000) {
        textInput.style.borderColor = 'var(--danger-color)';
    } else {
        textInput.style.borderColor = '#2d3542';
    }
});

// Speak Logic
speakBtn.addEventListener('click', () => {
    if (synth.speaking) {
        console.warn('System busy. Aborting previous stream.');
        synth.cancel();
    }

    if (textInput.value === '') {
        alert('ERROR: INPUT STREAM EMPTY');
        return;
    }

    const utterThis = new SpeechSynthesisUtterance(textInput.value);

    utterThis.onend = () => {
        visualizer.classList.remove('active');
        speakBtn.classList.remove('active');
        isSpeaking = false;
    };

    utterThis.onerror = () => {
        console.error('Speech synthesis error');
        visualizer.classList.remove('active');
        isSpeaking = false;
    };

    const selectedOption = voiceSelect.selectedOptions[0];
    if (selectedOption && !selectedOption.disabled) {
        const selectedVoiceName = selectedOption.getAttribute('data-name');
        utterThis.voice = voices.find(v => v.name === selectedVoiceName);
    }

    utterThis.rate = rateInput.value;
    utterThis.pitch = pitchInput.value;

    synth.speak(utterThis);

    // Visual Effects
    visualizer.classList.add('active');
    speakBtn.classList.add('active');
    isSpeaking = true;
});

// Stop Logic
stopBtn.addEventListener('click', () => {
    if (synth.speaking) {
        synth.cancel();
        visualizer.classList.remove('active');
        isSpeaking = false;
    }
});