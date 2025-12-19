
document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt-input');
    const generatedImage = document.getElementById('generated-image');
    const historyList = document.getElementById('history-list');

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value;
        if (!prompt) {
            alert('Please enter a prompt.');
            return;
        }

        // Add to history immediately with just the first line
        const listItem = document.createElement('li');
        
        listItem.textContent = prompt.split('\n')[0];
        
        listItem.dataset.fullPrompt = prompt;
        historyList.prepend(listItem);

        // API call
        try {
            generatedImage.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"; // a transparent 1x1 pixel gif
            generatedImage.alt = "Generating...";
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt }),
            });

            const data = await response.json();
            if (data.error) {
                alert(data.error);
                historyList.removeChild(listItem); // Remove the optimistic entry on error
            } else {
                generatedImage.src = `data:image/png;base64,${data.image}`;
                generatedImage.alt = "Generated Image";
                listItem.dataset.promptId = data.prompt_id; // Assign the ID after successful generation
            }
        } catch (error) {
            alert('An error occurred while generating the image.');
            historyList.removeChild(listItem);
        }
    });

    historyList.addEventListener('click', async (event) => {
        const targetLi = event.target.closest('li');
        if (targetLi) {
            const promptId = targetLi.dataset.promptId;
            const fullPrompt = targetLi.dataset.fullPrompt;

            // Preload the full prompt into the textarea
            if (fullPrompt) {
                promptInput.value = fullPrompt;
            }

            // Fetch the corresponding image
            if (promptId) {
                try {
                    generatedImage.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";
                    generatedImage.alt = "Loading image...";

                    const response = await fetch(`/get_image/${promptId}`);
                    const data = await response.json();
                    if (data.image) {
                        generatedImage.src = `data:image/png;base64,${data.image}`;
                        generatedImage.alt = "Generated Image";
                    } else {
                        generatedImage.alt = "Image not found for this prompt.";
                    }
                } catch (error) {
                    generatedImage.alt = "Error loading image.";
                }
            } else {
                // If the prompt hasn't been generated yet (e.g., clicked during generation)
                generatedImage.src = "";
                generatedImage.alt = "Image not yet generated for this new prompt.";
            }
        }
    });
});
