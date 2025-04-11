async function generateImage() {
            const prompt = document.getElementById('prompt').value;
            const loading = document.getElementById('loading');
            const resultDiv = document.getElementById('result');
            
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }

            loading.style.display = 'block';
            resultDiv.innerHTML = '';

            try {
                const response = await fetch('http://localhost:5000/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: prompt }),
                });

                if (!response.ok) {
                    throw new Error('Failed to generate image');
                }

                const data = await response.json();
                const img = document.createElement('img');
                img.id = 'generatedImage';
                img.src = `data:image/png;base64,${data.image}`;
                resultDiv.appendChild(img);

                // Add download button
                const downloadBtn = document.createElement('button');
                downloadBtn.textContent = 'Download Image';
                downloadBtn.onclick = function() {
                    const link = document.createElement('a');
                    link.href = img.src;
                    link.download = `generated-${Date.now()}.png`;
                    link.click();
                };
                resultDiv.appendChild(downloadBtn);

            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            } finally {
                loading.style.display = 'none';
            }
        }
    </script>


