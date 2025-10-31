// State management
let mediaRecorder;
let audioChunks = [];
let audioBlob;
let isRecording = false;

// DOM Elements
const recordBtn = document.getElementById('record-btn');
const stopBtn = document.getElementById('stop-btn');
const submitBtn = document.getElementById('submit-btn');
const tryAgainBtn = document.getElementById('try-again-btn');
const randomSentenceBtn = document.getElementById('random-sentence-btn');
const statusDiv = document.getElementById('status');
const resultsDiv = document.getElementById('results');
const expectedTextArea = document.getElementById('expected-text');
const languageSelect = document.getElementById('language');

// Event Listeners
recordBtn.addEventListener('click', startRecording);
stopBtn.addEventListener('click', stopRecording);
submitBtn.addEventListener('click', submitForEvaluation);
tryAgainBtn.addEventListener('click', resetApp);
randomSentenceBtn.addEventListener('click', loadRandomSentence);

// Check browser compatibility
window.addEventListener('DOMContentLoaded', () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showStatus('❌ Your browser does not support audio recording', 'error');
        recordBtn.disabled = true;
    }
});

/**
 * Start recording audio from microphone
 */
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                sampleRate: 16000
            } 
        });
        
        const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
            ? 'audio/webm;codecs=opus'
            : MediaRecorder.isTypeSupported('audio/webm') 
            ? 'audio/webm'
            : 'audio/ogg;codecs=opus';
        
        mediaRecorder = new MediaRecorder(stream, { mimeType });
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: mimeType });
            submitBtn.disabled = false;
            showStatus('✓ Recording complete! Click "Evaluate Pronunciation" to analyze your speech.', 'success');
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        submitBtn.disabled = true;
        
        showStatus('🔴 Recording in progress... Speak clearly!', 'recording');
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        showStatus('❌ Cannot access microphone. Please check permissions.', 'error');
    }
}

/**
 * Stop recording audio
 */
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        isRecording = false;
        recordBtn.disabled = false;
        stopBtn.disabled = true;
    }
}

/**
 * Submit audio for pronunciation evaluation
 */
async function submitForEvaluation() {
    const expectedText = expectedTextArea.value.trim();
    const language = languageSelect.value;
    
    if (!expectedText) {
        showStatus('❌ Please enter text to pronounce', 'error');
        return;
    }
    
    if (!audioBlob) {
        showStatus('❌ Please record audio first', 'error');
        return;
    }
    
    showStatus('⏳ Processing your pronunciation... This may take a moment.', 'processing');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
    
    const formData = new FormData();
    const extension = audioBlob.type.includes('webm') ? 'webm' : 'ogg';
    formData.append('audio', audioBlob, `recording.${extension}`);
    formData.append('expected_text', expectedText);
    formData.append('language', language);
    
    try {
        const response = await fetch('/api/evaluate', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }
        
        const result = await response.json();
        displayResults(result);
        showStatus('✓ Evaluation complete!', 'success');
        
        setTimeout(() => {
            statusDiv.classList.add('hidden');
        }, 3000);
        
    } catch (error) {
        console.error('Error:', error);
        showStatus(`❌ Error: ${error.message}. Please try again.`, 'error');
    } finally {
        submitBtn.innerHTML = '<span class="text-xl">✓</span><span>Evaluate Pronunciation</span>';
        submitBtn.disabled = false;
    }
}

/**
 * Load a random sentence from the database
 */
async function loadRandomSentence() {
    const language = languageSelect.value;
    
    randomSentenceBtn.disabled = true;
    randomSentenceBtn.innerHTML = '<span class="spinner"></span> Loading...';
    
    try {
        const response = await fetch(`/api/random-sentence?language=${language}`);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Failed to load sentence');
        }
        
        const data = await response.json();
        expectedTextArea.value = data.text;
        
        const difficultyColors = {
            easy: 'bg-green-100 text-green-800',
            medium: 'bg-yellow-100 text-yellow-800',
            hard: 'bg-red-100 text-red-800'
        };
        
        const difficultyClass = difficultyColors[data.difficulty] || 'bg-gray-100 text-gray-800';
        const difficultyBadge = `<span class="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase ml-2 ${difficultyClass}">${data.difficulty}</span>`;
        
        showStatus(`✓ Loaded: ${data.category} sentence ${difficultyBadge}`, 'success');
        
        setTimeout(() => {
            statusDiv.classList.add('hidden');
        }, 3000);
        
        expectedTextArea.style.transform = 'scale(1.02)';
        setTimeout(() => {
            expectedTextArea.style.transform = 'scale(1)';
        }, 200);
        
    } catch (error) {
        console.error('Error loading random sentence:', error);
        showStatus(`❌ ${error.message}`, 'error');
    } finally {
        randomSentenceBtn.disabled = false;
        randomSentenceBtn.innerHTML = '<span class="text-base">🎲</span><span>Random Sentence</span>';
    }
}

/**
 * Display evaluation results
 */
function displayResults(result) {
    resultsDiv.classList.remove('hidden');
    
    const accuracyEl = document.getElementById('overall-accuracy');
    const scoreBarEl = document.getElementById('score-bar');
    const accuracy = result.overall_accuracy;
    
    animateValue(accuracyEl, 0, accuracy, 1000);
    
    setTimeout(() => {
        scoreBarEl.style.width = `${accuracy}%`;
    }, 100);
    
    const transcriptEl = document.getElementById('transcript-text');
    transcriptEl.textContent = result.transcript || '(No speech detected)';
    
    const wordListEl = document.getElementById('word-list');
    wordListEl.innerHTML = '';
    
    if (result.word_comparisons && result.word_comparisons.length > 0) {
        result.word_comparisons.forEach((comparison, index) => {
            const wordDiv = createWordItem(comparison, index);
            wordListEl.appendChild(wordDiv);
        });
    } else {
        wordListEl.innerHTML = '<p class="text-center text-gray-500">No words to analyze</p>';
    }
    
    setTimeout(() => {
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

/**
 * Create a word item element
 */
function createWordItem(comparison, index) {
    const wordDiv = document.createElement('div');
    
    // Determine background color based on category
    const categoryColors = {
        correct: 'bg-green-50 border-l-green-500',
        similar: 'bg-yellow-50 border-l-yellow-500',
        incorrect: 'bg-red-50 border-l-red-500',
        missing: 'bg-gray-50 border-l-gray-500',
        extra: 'bg-blue-50 border-l-blue-500'
    };
    
    const colorClass = categoryColors[comparison.category] || 'bg-gray-50 border-l-gray-500';
    
    wordDiv.className = `flex justify-between items-center p-5 rounded-xl border-l-4 ${colorClass} hover:translate-x-1 hover:shadow-md transition-all duration-300 animate-slide-in`;
    wordDiv.style.animationDelay = `${index * 0.1}s`;
    
    // Build word text
    let wordText = '';
    if (comparison.expected_word && comparison.actual_word) {
        if (comparison.expected_word === comparison.actual_word) {
            wordText = `<strong>"${comparison.expected_word}"</strong> ✓`;
        } else {
            wordText = `Expected: <strong>"${comparison.expected_word}"</strong> → You said: <strong>"${comparison.actual_word}"</strong>`;
        }
    } else if (!comparison.actual_word) {
        wordText = `<strong>"${comparison.expected_word}"</strong> (missing)`;
    } else if (!comparison.expected_word) {
        wordText = `<strong>"${comparison.actual_word}"</strong> (extra word)`;
    }
    
    // Build IPA text
    let ipaText = '';
    if (comparison.expected_ipa && comparison.actual_ipa) {
        ipaText = `<div class="text-sm text-gray-600 font-mono bg-white/50 px-2 py-1 rounded inline-block mt-2">IPA: ${comparison.expected_ipa} → ${comparison.actual_ipa}</div>`;
    } else if (comparison.expected_ipa) {
        ipaText = `<div class="text-sm text-gray-600 font-mono bg-white/50 px-2 py-1 rounded inline-block mt-2">IPA: ${comparison.expected_ipa}</div>`;
    }
    
    wordDiv.innerHTML = `
        <div class="flex-1">
            <div class="text-lg font-semibold text-gray-800 mb-2">${wordText}</div>
            ${ipaText}
        </div>
        <div class="text-3xl font-bold text-gray-800 min-w-[80px] text-right">${comparison.similarity_score}%</div>
    `;
    
    return wordDiv;
}

/**
 * Show status message
 */
function showStatus(message, type = '') {
    statusDiv.innerHTML = message;
    statusDiv.classList.remove('hidden');
    
    // Remove all status classes
    statusDiv.className = 'text-center py-4 px-4 rounded-xl font-semibold text-base';
    
    // Add appropriate classes based on type
    if (type === 'recording') {
        statusDiv.classList.add('bg-yellow-100', 'text-yellow-800', 'animate-pulse-custom');
    } else if (type === 'processing') {
        statusDiv.classList.add('bg-blue-100', 'text-blue-800');
    } else if (type === 'error') {
        statusDiv.classList.add('bg-red-100', 'text-red-800');
    } else if (type === 'success') {
        statusDiv.classList.add('bg-green-100', 'text-green-800');
    }
}

/**
 * Animate a number value
 */
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = `${Math.round(current)}%`;
    }, 16);
}

/**
 * Reset the application for another attempt
 */
function resetApp() {
    audioBlob = null;
    audioChunks = [];
    
    recordBtn.disabled = false;
    stopBtn.disabled = true;
    submitBtn.disabled = true;
    
    resultsDiv.classList.add('hidden');
    statusDiv.classList.add('hidden');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        if (!recordBtn.disabled) {
            startRecording();
        }
    }
    
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        if (!stopBtn.disabled) {
            stopRecording();
        }
    }
    
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        if (!submitBtn.disabled) {
            submitForEvaluation();
        }
    }
});

// Handle page visibility
document.addEventListener('visibilitychange', () => {
    if (document.hidden && isRecording) {
        stopRecording();
        showStatus('Recording stopped (tab switched)', 'error');
    }
});