#!/usr/bin/env python3
"""
Stable Diffusion Image Generator API using DreamShaper model
"""
import os
import base64
import logging
from io import BytesIO

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class ImageGenerator:
    def __init__(self, model_name="Lykon/DreamShaper"):
        """Initialize the image generator with specified model."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.pipe = None
        self.load_model()

    def load_model(self):
        """Load the Stable Diffusion model."""
        logger.info(f"Loading model {self.model_name} on {self.device}...")
        torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_name,
            torch_dtype=torch_dtype,
            safety_checker=None,
            requires_safety_checker=False
        ).to(self.device)
        
        # Optimizations
        if self.device == "cuda":
            self.pipe.enable_xformers_memory_efficient_attention()
        self.pipe.enable_attention_slicing()

    def generate_image(self, prompt):
        """Generate an image from text prompt and return base64 string."""
        logger.info(f"Generating image for prompt: '{prompt}'")
        
        image = self.pipe(prompt).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Initialize generator when starting the server
generator = ImageGenerator()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        image_data = generator.generate_image(prompt)
        return jsonify({"image": image_data})
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return jsonify({"error": "Image generation failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
