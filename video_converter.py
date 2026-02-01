#!/usr/bin/env python3
"""
Video Converter: Convert 16:9 aspect ratio videos to 9:16 aspect ratio
"""

import sys
from moviepy.editor import VideoFileClip
import argparse
import os


def convert_16_9_to_9_16(input_path, output_path, method='crop'):
    """
    Convert a 16:9 video to 9:16 aspect ratio.
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file
        method: 'crop' (center crop) or 'scale' (scale and pad with black bars)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print(f"Loading video: {input_path}")
    clip = VideoFileClip(input_path)
    
    original_width, original_height = clip.size
    original_aspect = original_width / original_height
    
    print(f"Original dimensions: {original_width}x{original_height} (aspect ratio: {original_aspect:.2f})")
    
    if method == 'crop':
        # Crop method: Take center portion of 16:9 video to make it 9:16
        # For 9:16 output: width/height = 9/16, so width = (9/16) * height
        # Strategy: Calculate the maximum 9:16 crop that fits within the original video
        
        # Calculate what dimensions we can get for 9:16 aspect ratio
        # Option 1: Use full height, crop width
        crop_width_from_height = original_height * 9 / 16
        # Option 2: Use full width, crop height  
        crop_height_from_width = original_width * 16 / 9
        
        # Choose the option that gives us the largest crop area
        if crop_width_from_height <= original_width:
            # Use full height, crop width (most common for 16:9 input)
            crop_width = int(crop_width_from_height)
            crop_height = original_height
        else:
            # Use full width, crop height (fallback for unusual aspect ratios)
            crop_width = original_width
            crop_height = int(crop_height_from_width)
        
        # Ensure crop dimensions don't exceed original dimensions
        crop_width = min(crop_width, original_width)
        crop_height = min(crop_height, original_height)
        
        # Calculate center-aligned crop coordinates
        # Center point of original video
        x_center = original_width / 2.0
        y_center = original_height / 2.0
        
        # Calculate crop boundaries (centered)
        x1 = x_center - crop_width / 2.0
        y1 = y_center - crop_height / 2.0
        x2 = x_center + crop_width / 2.0
        y2 = y_center + crop_height / 2.0
        
        # Ensure crop coordinates are within bounds (clamp to video boundaries)
        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(original_width, int(x2))
        y2 = min(original_height, int(y2))
        
        # Recalculate crop dimensions from clamped coordinates to ensure exact dimensions
        actual_crop_width = x2 - x1
        actual_crop_height = y2 - y1
        
        # Adjust to maintain 9:16 aspect ratio if needed
        target_aspect = 9 / 16
        actual_aspect = actual_crop_width / actual_crop_height if actual_crop_height > 0 else target_aspect
        
        if abs(actual_aspect - target_aspect) > 0.01:  # If aspect ratio is off by more than 1%
            # Adjust to exact 9:16
            if actual_crop_width / actual_crop_height > target_aspect:
                # Too wide, reduce width
                actual_crop_width = int(actual_crop_height * target_aspect)
                x1 = int(x_center - actual_crop_width / 2)
                x2 = x1 + actual_crop_width
            else:
                # Too tall, reduce height
                actual_crop_height = int(actual_crop_width / target_aspect)
                y1 = int(y_center - actual_crop_height / 2)
                y2 = y1 + actual_crop_height
            
            # Final bounds check
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(original_width, x2)
            y2 = min(original_height, y2)
            actual_crop_width = x2 - x1
            actual_crop_height = y2 - y1
        
        print(f"Cropping to: {actual_crop_width}x{actual_crop_height} (9:16 aspect ratio)")
        print(f"Crop region (center-aligned): ({x1}, {y1}) to ({x2}, {y2})")
        print(f"Center point: ({x_center:.1f}, {y_center:.1f})")
        
        # Crop the video with center alignment
        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        
        # Scale to a standard 9:16 resolution (1080x1920) for better quality
        target_width = 1080
        target_height = 1920
        
        # Calculate scale factor to reach target resolution
        scale_factor = min(target_width / actual_crop_width, target_height / actual_crop_height) if actual_crop_width > 0 else 1
        
        final_width = int(actual_crop_width * scale_factor)
        final_height = int(actual_crop_height * scale_factor)
        
        # Ensure dimensions are even (required for some codecs)
        final_width = final_width if final_width % 2 == 0 else final_width + 1
        final_height = final_height if final_height % 2 == 0 else final_height + 1
        
        # Ensure final aspect ratio is exactly 9:16
        final_aspect = final_width / final_height if final_height > 0 else 9/16
        if abs(final_aspect - (9/16)) > 0.01:
            # Adjust to exact 9:16
            final_height = int(final_width * 16 / 9)
            final_height = final_height if final_height % 2 == 0 else final_height + 1
        
        print(f"Scaling to: {final_width}x{final_height} (aspect ratio: {final_width/final_height:.4f})")
        final_clip = cropped_clip.resize((final_width, final_height))
        
    elif method == 'scale':
        # Scale method: Scale video to fit 9:16 and add black bars if needed
        # Scale the 16:9 video to fit within a 9:16 frame while maintaining aspect ratio
        # The video will be scaled down and black bars added on top/bottom
        
        # Target 9:16 dimensions - use a standard resolution like 1080x1920
        # Scale based on width to fit the 9:16 frame
        target_width = 1080  # Standard 9:16 width
        target_height = 1920  # Standard 9:16 height
        
        # Calculate scale factor to fit 16:9 video into 9:16 width
        # The video width should fit within target_width
        scale_factor = target_width / original_width
        
        scaled_width = int(original_width * scale_factor)
        scaled_height = int(original_height * scale_factor)
        
        # Ensure dimensions are even
        scaled_width = scaled_width if scaled_width % 2 == 0 else scaled_width + 1
        scaled_height = scaled_height if scaled_height % 2 == 0 else scaled_height + 1
        
        # Resize video
        resized_clip = clip.resize((scaled_width, scaled_height))
        
        # Create 9:16 canvas
        final_width = target_width
        final_height = target_height
        
        # Center the video on the canvas with black bars on top and bottom
        final_clip = resized_clip.margin(
            top=(final_height - scaled_height) // 2,
            bottom=(final_height - scaled_height) // 2,
            left=0,
            right=0,
            color=(0, 0, 0)
        )
        
        print(f"Scaling to: {final_width}x{final_height} (9:16 aspect ratio)")
        print(f"Video scaled to: {scaled_width}x{scaled_height} with black bars on top/bottom")
    else:
        raise ValueError(f"Unknown method: {method}. Use 'crop' or 'scale'")
    
    print(f"Final dimensions: {final_clip.size[0]}x{final_clip.size[1]}")
    print(f"Writing output to: {output_path}")
    
    # Write the output video
    final_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Clean up
    clip.close()
    final_clip.close()
    
    print("Conversion completed successfully!")


def main():
    parser = argparse.ArgumentParser(
        description='Convert 16:9 aspect ratio videos to 9:16 aspect ratio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_converter.py input.mp4 output.mp4
  python video_converter.py input.mp4 output.mp4 --method scale
        """
    )
    
    parser.add_argument('input', help='Input video file path')
    parser.add_argument('output', help='Output video file path')
    parser.add_argument(
        '--method',
        choices=['crop', 'scale'],
        default='crop',
        help='Conversion method: crop (center crop, default) or scale (scale and pad)'
    )
    
    args = parser.parse_args()
    
    try:
        convert_16_9_to_9_16(args.input, args.output, args.method)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
