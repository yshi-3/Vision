async function generateImage() {
    const userInput = document.getElementById('userInput').value;
    const loading = document.getElementById('loading');
    const output = document.getElementById('output');

    if (!userInput) {
        alert('Please enter a description!');
        return;
    }

    loading.style.display = 'block';
    output.innerHTML = '';

    try {
        const response = await fetch('http://localhost:3000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: userInput }),
        });

        const data = await response.json();

        if (data.imageUrl) {
            output.innerHTML = `<img src="${data.imageUrl}" alt="Generated Image">`;
        } else {
            output.innerHTML = '<p>Failed to generate image. Please try again.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        output.innerHTML = '<p>An error occurred. Please try again.</p>';
    } finally {
        loading.style.display = 'none';
    }
}