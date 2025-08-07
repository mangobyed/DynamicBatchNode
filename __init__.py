import torch
import torch.nn.functional as F


class DynamicImageBatch:
    """
    A ComfyUI node that dynamically creates image inputs as you connect them.
    Based on the cozy-comfyui dynamic input example.
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return input types. Start with default inputs that will be managed by JavaScript.
        """
        return {
            "required": {
                "input_count": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 20,
                    "step": 1,
                    "display": "number"
                }),
                "method": (["lanczos", "nearest", "linear", "bilinear", "bicubic"], {
                    "default": "lanczos"
                }),
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            },
            "optional": {}
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("batched_images",)
    FUNCTION = "batch_images"
    CATEGORY = "image/batch"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """This will trigger UI updates when input_count changes"""
        return kwargs.get("input_count", 2)
    
    @classmethod
    def VALIDATE_INPUTS(cls, input_count, method, **kwargs):
        """Validate inputs before execution"""
        # Validate input_count
        if not isinstance(input_count, int) or input_count < 1 or input_count > 20:
            return f"input_count must be an integer between 1 and 20, got {input_count}"
        
        # Validate method
        valid_methods = ["lanczos", "nearest", "linear", "bilinear", "bicubic"]
        if method not in valid_methods:
            return f"method must be one of {valid_methods}, got '{method}'"
        
        # The validation is too strict for ComfyUI's execution model
        # Let the main function handle missing inputs with better error messages
        return True

    def batch_images(self, input_count, method, **kwargs):
        """
        Batch multiple images together based on the input_count.
        Only processes the number of images specified by input_count.
        """
        images = []
        missing_inputs = []
        
        # Collect images based on input_count and track missing ones
        for i in range(1, input_count + 1):
            image_key = f"image_{i}"
            if image_key in kwargs and kwargs[image_key] is not None:
                # Validate that it's actually an image tensor
                image = kwargs[image_key]
                if not isinstance(image, torch.Tensor):
                    raise ValueError(f"Input {image_key} is not a valid image tensor. Expected torch.Tensor, got {type(image).__name__}")
                
                # Check tensor dimensions (should be 4D: batch, height, width, channels)
                if len(image.shape) != 4:
                    raise ValueError(f"Input {image_key} has invalid dimensions. Expected 4D tensor (batch, height, width, channels), got shape {image.shape}")
                
                # Check if it has the right number of channels (should be 3 for RGB or 1 for grayscale)
                if image.shape[3] not in [1, 3, 4]:  # RGB, Grayscale, or RGBA
                    raise ValueError(f"Input {image_key} has invalid number of channels. Expected 1, 3, or 4 channels, got {image.shape[3]}")
                
                images.append(image)
            else:
                missing_inputs.append(image_key)
        
        # Strict validation: ALL specified inputs must be connected
        if missing_inputs:
            if len(missing_inputs) == input_count:
                raise ValueError(f"No images provided! Please connect images to all {input_count} input sockets. Missing: {', '.join(missing_inputs)}")
            else:
                missing_count = len(missing_inputs)
                connected_count = len(images)
                raise ValueError(f"Missing {missing_count} image(s)! Expected {input_count} images, but only {connected_count} connected. Missing inputs: {', '.join(missing_inputs)}. Please connect images to ALL input sockets.")
        
        # Validate we have at least one image
        if not images:
            raise ValueError("No valid images found. Please connect valid image inputs.")
        
        # Double-check we have exactly the expected number of images
        if len(images) != input_count:
            raise ValueError(f"Input count mismatch! Expected exactly {input_count} images, but got {len(images)}. Please ensure all inputs are properly connected.")
        
        # If only one image, return it as is
        if len(images) == 1:
            return (images[0],)
        
        # Get the target size from the first image
        target_height = images[0].shape[1]
        target_width = images[0].shape[2]
        target_channels = images[0].shape[3]
        
        print(f"Dynamic Image Batch: Processing {len(images)} images, target size: {target_width}x{target_height}x{target_channels}")
        
        # Resize all images to match the first image's dimensions
        resized_images = []
        for idx, img in enumerate(images):
            try:
                # Check channel compatibility
                if img.shape[3] != target_channels:
                    raise ValueError(f"Channel mismatch: image_{idx+1} has {img.shape[3]} channels, but image_1 has {target_channels} channels. All images must have the same number of channels.")
                
                if img.shape[1] != target_height or img.shape[2] != target_width:
                    print(f"Resizing image_{idx+1} from {img.shape[2]}x{img.shape[1]} to {target_width}x{target_height}")
                    
                    # Convert method name to PyTorch mode
                    if method == "lanczos":
                        mode = "bilinear"  # PyTorch doesn't have lanczos, use bilinear as fallback
                    elif method == "nearest":
                        mode = "nearest"
                    elif method == "linear" or method == "bilinear":
                        mode = "bilinear"
                    elif method == "bicubic":
                        mode = "bicubic"
                    else:
                        mode = "bilinear"
                    
                    # Resize image using interpolation
                    # img shape: [batch, height, width, channels]
                    # F.interpolate expects: [batch, channels, height, width]
                    img_permuted = img.permute(0, 3, 1, 2)
                    
                    try:
                        resized = F.interpolate(
                            img_permuted, 
                            size=(target_height, target_width), 
                            mode=mode,
                            align_corners=False if mode != "nearest" else None
                        )
                        # Permute back to original format
                        resized = resized.permute(0, 2, 3, 1)
                        resized_images.append(resized)
                    except Exception as e:
                        raise ValueError(f"Failed to resize image_{idx+1} using {method} interpolation: {str(e)}")
                else:
                    resized_images.append(img)
                    
            except Exception as e:
                raise ValueError(f"Error processing image_{idx+1}: {str(e)}")
        
        # Concatenate all images along the batch dimension
        try:
            batched = torch.cat(resized_images, dim=0)
            print(f"Dynamic Image Batch: Successfully batched {len(resized_images)} images into tensor of shape {batched.shape}")
            return (batched,)
        except Exception as e:
            raise ValueError(f"Failed to batch images together: {str(e)}. Make sure all images are compatible.")


# Set the web directory for JavaScript extensions
WEB_DIRECTORY = "./js"

# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DynamicImageBatch": DynamicImageBatch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicImageBatch": "Dynamic Image Batch",
}