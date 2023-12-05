document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('startCamera').addEventListener('click', async () => {

        try {
            const constraints = {
              video: {
                facingMode: "environment"
              },
            };
            const stream = await navigator.mediaDevices.getUserMedia(constraints);

            const video = document.getElementById('cameraFeed');
            video.srcObject = stream;

            const sendVideoToBackend = async () => {

                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL('image/jpeg');
                const timestamp = Date.now();
                const csrftoken = getCookie('csrftoken');

                //mettre adresse ip locale de son ordi ->ipconfig
                const response = await fetch('https://192.168.1.95:8080/back/yoloApi', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,  // Include the CSRF token in the headers

                    },
                    body: JSON.stringify({ imageData, timestamp }),
                });
// Si la réponse est un fichier MP3, téléchargez-le
                if (response.ok) {
                    const contentType = response.headers.get('content-type');

                    if (contentType === 'application/zip') {
                        const zipBlob = await response.blob();

                        // Use JSZip to extract files from the ZIP
                        const zip = new JSZip();
                        const zipContent = await zip.loadAsync(zipBlob);
                        console.log(zipBlob);
            const audioPlayer = document.getElementById('audioPlayer');

                        // Assuming each file in the ZIP is an MP3
                        zipContent.forEach((relativePath, zipEntry) => {
                            console.log(zipEntry.name);

                            if (zipEntry.dir === false && zipEntry.name.endsWith('.wav')) {
                // Create an Audio element and play the WAV
                const wavData = zipEntry._data;

                // Create an Audio element
                const audio = new Audio();
                audio.src = URL.createObjectURL(new Blob([wavData], { type: 'audio/wav' }));

                // Update the existing audio player or append a new one
                audioPlayer.src = audio.src;
                audioPlayer.load();
                audioPlayer.play().catch(error => console.error("Error playing audio:", error));
            }
                        });
                    } else {
                        console.error("The response is not a ZIP file.");
                    }
                } else {
                    console.error("Error in response:", response.status, response.statusText);
                }
            };

            setInterval(sendVideoToBackend, 10000);
        } catch (error) {
            console.error("Erreur lors de l'accès à la caméra : ", error);
        }

    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
