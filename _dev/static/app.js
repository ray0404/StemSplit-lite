const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const progressArea = document.getElementById('progress-area');
const statusText = document.getElementById('status-text');
const resultsArea = document.getElementById('results-area');
const linksContainer = document.getElementById('links-container');
const resetBtn = document.getElementById('reset-btn');

// Drag and Drop events
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleUpload(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        handleUpload(fileInput.files[0]);
    }
});

resetBtn.addEventListener('click', () => {
    resultsArea.classList.add('hidden');
    dropZone.classList.remove('hidden');
    fileInput.value = '';
});

async function handleUpload(file) {
    dropZone.classList.add('hidden');
    progressArea.classList.remove('hidden');
    statusText.textContent = "Uploading " + file.name + "...";

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        const songName = data.song_name;
        
        statusText.textContent = "Processing... (This may take a minute)";
        pollStatus(songName);

    } catch (error) {
        console.error(error);
        statusText.textContent = "Error: " + error.message;
        setTimeout(() => {
            progressArea.classList.add('hidden');
            dropZone.classList.remove('hidden');
        }, 3000);
    }
}

async function pollStatus(songName) {
    const intervalId = setInterval(async () => {
        try {
            const response = await fetch(`/status/${songName}`);
            const data = await response.json();

            if (data.status === 'completed') {
                clearInterval(intervalId);
                showResults(songName, data.files);
            }
        } catch (error) {
            console.error("Polling error", error);
        }
    }, 2000); // Poll every 2 seconds
}

function showResults(songName, files) {
    progressArea.classList.add('hidden');
    resultsArea.classList.remove('hidden');
    linksContainer.innerHTML = '';

    files.forEach(file => {
        const link = document.createElement('a');
        link.href = `/download/${songName}/${file}`;
        link.textContent = `Download ${file}`;
        link.classList.add('download-link');
        link.setAttribute('download', '');
        linksContainer.appendChild(link);
    });
}
