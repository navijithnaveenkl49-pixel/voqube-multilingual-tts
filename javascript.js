const synth = window.speechSynthesis;
const textInput = document.querySelector('#text-input');
const voiceSelect = document.querySelector('#voice-select');
const speakBtn = document.querySelector('#speak-btn');

let voices = [];

function getVoices() {
    voices = synth.getVoices();
    voiceSelect.innerHTML = ''; 
    voices.forEach((voice) => {
        const option = document.createElement('option');
        option.textContent = `${voice.name} (${voice.lang})`;
        option.setAttribute('data-lang', voice.lang);
        option.setAttribute('data-name', voice.name);
        voiceSelect.appendChild(option);
    });
}

if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = getVoices;
}

speakBtn.addEventListener('click', () => {
    if (synth.speaking) {
        console.error('Already speaking...');
        return;
    }

    if (textInput.value !== '') {
        const utterThis = new SpeechSynthesisUtterance(textInput.value);
        
        const selectedVoiceName = voiceSelect.selectedOptions[0].getAttribute('data-name');
        utterThis.voice = voices.find(v => v.name === selectedVoiceName);

        synth.speak(utterThis);
    }
});