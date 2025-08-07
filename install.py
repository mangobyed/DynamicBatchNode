#!/usr/bin/env python3
"""
Installation script for Dynamic Image Batch Node
This script helps verify the installation and provides helpful information.
"""

import os
import sys
import platform

def check_installation():
    """Check if the node is properly installed"""
    print("🔍 Checking Dynamic Image Batch Node installation...")
    
    # Check if we're in the right directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Installation directory: {current_dir}")
    
    # Check for required files
    required_files = [
        "__init__.py",
        "js/dynamic_image_batch.js",
        "README.md",
        "LICENSE"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    # Check if we're in ComfyUI custom_nodes directory
    parent_dir = os.path.basename(os.path.dirname(current_dir))
    if parent_dir == "custom_nodes":
        print("✅ Located in ComfyUI custom_nodes directory")
    else:
        print(f"⚠️  Not in custom_nodes directory (currently in {parent_dir})")
        print("   Make sure to place this in ComfyUI/custom_nodes/")
    
    # System information
    print(f"\n💻 System Information:")
    print(f"   Python: {sys.version}")
    print(f"   Platform: {platform.system()} {platform.release()}")
    
    # Installation summary
    if missing_files:
        print(f"\n❌ Installation incomplete. Missing files: {', '.join(missing_files)}")
        return False
    else:
        print(f"\n✅ Installation appears complete!")
        print(f"   Next steps:")
        print(f"   1. Restart ComfyUI")
        print(f"   2. Look for 'Dynamic Image Batch' in the image/batch category")
        print(f"   3. Check the README.md for usage instructions")
        return True

if __name__ == "__main__":
    print("🚀 Dynamic Image Batch Node Installation Checker")
    print("=" * 50)
    
    success = check_installation()
    
    if success:
        print("\n🎉 Ready to use! Restart ComfyUI to load the node.")
    else:
        print("\n⚠️  Please fix the missing files and try again.")
        sys.exit(1)