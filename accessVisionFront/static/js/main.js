document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('startCamera').addEventListener('click', async () => {
        
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
                const timestamp = Date.now();

                //mettre adresse ip locale de son ordi ->ipconfig
                const response = await fetch('https://192.168.1.28:8000/back/yoloApi', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ imageData, timestamp }),
                });
                const result = await response.text();
            };
            
            setInterval(sendVideoToBackend, 10000);
        } catch (error) {
            console.error("Erreur lors de l'accès à la caméra : ", error);
        }
        
    }); 
});
