const synth = window.speechSynthesis;
const textInput = document.getElementById('text-input');
const speakBtn = document.getElementById('speak-btn');

speakBtn.addEventListener('click', () => {
    const textValue = textInput.value;
    const utterThis = new SpeechSynthesisUtterance(textValue);
    synth.speak(utterThis);

    fetch('https://texttovoicegenerator.unaux.com/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textValue })
    })
    .then(response => response.json())
    .then(data => console.log('Backend Response:', data))
    .catch(err => console.error('Connection failed:', err));
});