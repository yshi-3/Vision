async function generateImage() {
            /*
            Original: const prompt = document.getElementById('prompt').value;
            Problem: Did not match the input field ID provided in the updated version (maybe? IDK if its right first but then you changed the id)
            Solution: Change the id to the appropriate input field ID
            */
            const prompt = document.getElementById('userInput').value;
            const loading = document.getElementById('loading');
            /*
            Original: const resultDiv = document.getElementById('result');
            Problem: Did not match the input div ID provided in the updated version (maybe? IDK if its right first but then you changed the id)
            Solution: Change the id to the appropriate div ID
            */
            const resultDiv = document.getElementById('output');
            
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }

            loading.style.display = 'block';
            resultDiv.innerHTML = '';

            try {
                const response = await fetch('https://image-generator.onrender.com/generate', { //original: } Problem: I think you can see the problem here...
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


