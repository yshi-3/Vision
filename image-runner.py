#!/usr/bin/env python3
"""
Stable Diffusion Image Generator using DreamShaper model

This script generates images from text prompts using the DreamShaper model
and outputs them as base64-encoded strings or saves to file.
"""

import argparse
import base64
import logging
import sys
import time
from io import BytesIO
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, model_name="Lykon/DreamShaper", device=None):
        """
        Initialize the image generator with specified model.
        
        Args:
            model_name (str): Name of the Stable Diffusion model to use
            device (str): Device to use ('cuda', 'mps', 'cpu'). Auto-detects if None.
        """
        self.model_name = model_name
        self.device = self._determine_device(device)
        self.pipe = None
        
    def _determine_device(self, device):
        """Determine the best available device."""
        if device:
            return device
            
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    
    def load_model(self):
        """Load the Stable Diffusion model."""
        logger.info(f"Loading model {self.model_name} on {self.device}...")
        start_time = time.time()
        
        torch_dtype = torch.float16 if self.device in ["cuda", "mps"] else torch.float32
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_name,
            torch_dtype=torch_dtype
        ).to(self.device)
        
        logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds")
    
    def generate_image(self, prompt, output_format="base64", output_path=None):
        """
        Generate an image from a text prompt.
        
        Args:
            prompt (str): Text prompt for image generation
            output_format (str): Output format ('base64' or 'pil')
            output_path (str): Optional path to save image file
            
        Returns:
            Base64 string or PIL Image depending on output_format
        """
        if not self.pipe:
            self.load_model()
            
        logger.info(f"Generating image for prompt: '{prompt}'")
        start_time = time.time()
        
        try:
            image = self.pipe(prompt).images[0]
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise RuntimeError(f"Image generation failed: {str(e)}")
        
        generation_time = time.time() - start_time
        logger.info(f"Image generated in {generation_time:.2f} seconds")
        
        if output_path:
            self._save_image(image, output_path)
        
        if output_format == "base64":
            return self._image_to_base64(image)
        return image
    
    def _save_image(self, image, output_path):
        """Save image to file."""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path)
            logger.info(f"Image saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save image: {str(e)}")
            raise RuntimeError(f"Failed to save image: {str(e)}")
    
    def _image_to_base64(self, image):
        """Convert PIL Image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate images using Stable Diffusion DreamShaper model"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Text prompt for image generation"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save the generated image"
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["auto", "cuda", "mps", "cpu"],
        default="auto",
        help="Device to use for generation"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        device = None if args.device == "auto" else args.device
        generator = ImageGenerator(device=device)
        
        if args.output:
            # Save to file and get base64
            image_data = generator.generate_image(
                args.prompt,
                output_format="base64",
                output_path=args.output
            )
            print(f"Image generated and saved to {args.output}")
        else:
            # Just get base64
            image_data = generator.generate_image(args.prompt)
            print(image_data)
            
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

