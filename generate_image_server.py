# stable_diffusion_service.py
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO
import logging
from flask import Flask, request, jsonify
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)

# Global model variable
pipe = None

def load_model():
    global pipe
    try:
        # Detect hardware
        if torch.cuda.is_available():
            device = "cuda"
            torch_dtype = torch.float16
        elif torch.backends.mps.is_available():
            device = "mps"
            torch_dtype = torch.float32  # MPS doesn't fully support float16
        else:
            device = "cpu"
            torch_dtype = torch.float32
            
        logger.info(f"Initializing on device: {device}")

        # Load model with memory optimizations
        logger.info("Loading DreamShaper model...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "Lykon/DreamShaper",
            torch_dtype=torch_dtype,
            safety_checker=None  # Disable safety checker for more prompts
        )
        pipe = pipe.to(device)

        # Apply optimizations
        if device == "cuda":
            try:
                pipe.enable_xformers_memory_efficient_attention()
            except:
                logger.warning("Xformers not available, using default attention")
            pipe.enable_attention_slicing()
            pipe.enable_model_cpu_offload()
        
        logger.info("Model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}", exc_info=True)
        return False

@app.route('/generate', methods=['POST'])
def generate():
    global pipe
    if not pipe:
        return jsonify({"error": "Model not loaded"}), 503

    try:
        # Get prompt from request
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({"error": "Empty prompt"}), 400

        logger.info(f"Generating image for: {prompt[:50]}...")

        # Generate image
        with torch.autocast(pipe.device.type):
            image = pipe(
                prompt,
                height=512,
                width=512,
                num_inference_steps=25,
                guidance_scale=7.5
            ).images[0]

        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({
            "image": img_str,
            "model": "DreamShaper",
            "resolution": "512x512"
        })

    except Exception as e:
        logger.error(f"Generation failed: {str(e)}", exc_info=True)
        return jsonify({"error": "Image generation failed"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ready" if pipe else "loading",
        "device": str(pipe.device) if pipe else "none",
        "memory": f"{torch.cuda.memory_allocated()/1024**3:.2f}GB" if torch.cuda.is_available() else "unknown"
    })

if __name__ == "__main__":
    # Load model first
    if not load_model():
        logger.error("Failed to load model - exiting")
        sys.exit(1)

    # Start Flask development server
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True,
        debug=False
    )
