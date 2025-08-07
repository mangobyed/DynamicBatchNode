# Dynamic Image Batch Node for ComfyUI

A powerful ComfyUI custom node that allows dynamic batching of multiple images with configurable input counts and interpolation methods.

![Dynamic Image Batch Demo](https://img.shields.io/badge/ComfyUI-Custom%20Node-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **🔢 Dynamic Input Count**: Specify exactly how many image inputs you need (1-20)
- **🎛️ Real-time UI Updates**: Image inputs appear/disappear instantly when changing input count
- **🖼️ Smart Image Processing**: Automatically resizes images to match the first image's dimensions
- **🔧 Multiple Interpolation Methods**: lanczos, nearest, linear, bilinear, bicubic
- **⚠️ Comprehensive Error Handling**: Clear error messages for missing or invalid inputs
- **✅ Strict Validation**: Ensures all specified inputs are connected before processing

## Installation

### Method 1: Git Clone (Recommended)

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/MoldenAI/DynamicBatchNode.git
   ```

3. Restart ComfyUI

### Method 2: Manual Download

1. Download the repository as a ZIP file
2. Extract it to `ComfyUI/custom_nodes/DynamicBatchNode/`
3. Restart ComfyUI

## Usage

1. **Add the Node**: Search for "Dynamic Image Batch" in the node menu under `image/batch` category

2. **Set Input Count**: Adjust the `input_count` parameter (1-20) to specify how many images you want to batch

3. **Connect Images**: Connect your images to the dynamically created `image_1`, `image_2`, etc. inputs

4. **Choose Method**: Select your preferred interpolation method:
   - `lanczos`: High-quality interpolation (default)
   - `nearest`: Fastest, pixelated results
   - `bilinear`: Good balance of speed and quality
   - `bicubic`: Higher quality, slower
   - `linear`: Basic linear interpolation

5. **Get Output**: The node outputs a batched tensor containing all processed images

## Example Workflow

```
Load Image → image_1 ┐
Load Image → image_2 ├─ Dynamic Image Batch → Preview Image
Load Image → image_3 ┘     (input_count: 3)
```

## Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `input_count` | INT | 1-20 | 2 | Number of image inputs to create |
| `method` | STRING | lanczos/nearest/linear/bilinear/bicubic | lanczos | Interpolation method for resizing |

## Error Handling

The node provides clear error messages for common issues:

- **Missing Images**: "Missing X image(s)! Expected Y images, but only Z connected."
- **Invalid Tensors**: "Input image_X is not a valid image tensor."
- **Dimension Mismatch**: "Input image_X has invalid dimensions."
- **Channel Mismatch**: "Channel mismatch: all images must have the same number of channels."

## Technical Details

### Input Processing
- Accepts standard ComfyUI IMAGE tensors
- Supports RGB (3 channels), Grayscale (1 channel), and RGBA (4 channels) images
- Automatically resizes all images to match the first image's dimensions
- Maintains aspect ratio during resizing

### Output Format
- Returns a single IMAGE tensor with all images batched along the batch dimension
- Output shape: `[total_batch_size, height, width, channels]`
- Compatible with all standard ComfyUI image processing nodes

### Performance
- Efficient tensor operations using PyTorch
- Minimal memory overhead
- Real-time UI updates via JavaScript extension

## Requirements

- ComfyUI (latest version)
- PyTorch (included with ComfyUI)
- Modern web browser (for JavaScript features)

## Development

### File Structure
```
DynamicBatchNode/
├── __init__.py              # Main node implementation
├── js/
│   └── dynamic_image_batch.js  # JavaScript for dynamic UI
├── README.md                # This file
└── LICENSE                  # MIT License
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with different input combinations
5. Submit a pull request

## Troubleshooting

### Node Not Appearing
- Ensure the folder is in `ComfyUI/custom_nodes/`
- Restart ComfyUI completely
- Check the console for any error messages

### JavaScript Features Not Working
- Clear your browser cache (Ctrl+F5)
- Check browser console for JavaScript errors
- Ensure ComfyUI is updated to the latest version

### Input Count Not Updating
- The JavaScript extension requires a modern browser
- Try refreshing the page
- Check that the `js` folder is present in the node directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Dynamic input count functionality
- Multiple interpolation methods
- Comprehensive error handling
- Real-time UI updates

## Support

If you encounter any issues or have suggestions:

1. Check the [Issues](https://github.com/MoldenAI/DynamicBatchNode/issues) page
2. Create a new issue with:
   - ComfyUI version
   - Browser type and version
   - Detailed description of the problem
   - Screenshots if applicable

## Credits

Developed by [MoldenAI](https://github.com/MoldenAI) for the ComfyUI community.

---

⭐ If you find this node useful, please consider starring the repository!