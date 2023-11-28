document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('startCamera').addEventListener('click', async () => {
        console.log("ça passe dans l'envoi de vidéo");
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            const video = document.getElementById('cameraFeed');
            video.srcObject = stream;

            const sendVideoToBackend = async () => {
                
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL('image/jpeg');
                

                const response = await fetch('https://127.0.0.1:8000/back/test-backend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ imageData }),
                });
                const result = await response.text();
                console.log(result);
            };

            setInterval(sendVideoToBackend, 1000);
        } catch (error) {
            console.error("Erreur lors de l'accès à la caméra : ", error);
        }
    });
});
