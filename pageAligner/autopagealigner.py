import os
import cv2
import numpy as np
from deskew import determine_skew
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from config import PopplerExeConfig

# Rotate a numpy image by angle (in degrees)
def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rot_mat = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(image, 
    rot_mat, (w, h), 
    flags=cv2.INTER_LINEAR,
    borderMode=cv2.BORDER_REPLICATE
    )
    return rotated

# ──────────────────────────────────────────────
# Convert PDF pages to list of PIL images
def convert_pdf_as_image(pdf_path: str):
    return convert_from_path(
        pdf_path,
        poppler_path=PopplerExeConfig.poppler_path,
        thread_count=PopplerExeConfig.thread_count,
        dpi=PopplerExeConfig.dpi
    )

# ──────────────────────────────────────────────
# Get skew angles (in degrees) for all pages
def find_all_page_rotation(pdf_path: str):
    pil_images = convert_pdf_as_image(pdf_path)
    numpy_images = [np.asarray(img) for img in pil_images]

    with ThreadPoolExecutor(max_workers=PopplerExeConfig.thread_count) as executor:
        skew_angles = list(executor.map(determine_skew, numpy_images))

    return skew_angles, numpy_images, pil_images

# ──────────────────────────────────────────────
# Deskew only pages with skew angle beyond threshold
def deskew_misaligned_pages(skew_angles, numpy_images, threshold=0.5):
    for i, angle in enumerate(skew_angles):
        if abs(angle) > threshold:
            print(f"Deskewing page {i + 1} (angle: {angle:.2f})...")
            corrected = rotate_image(numpy_images[i], angle)
            numpy_images[i] = corrected
            new_angle = determine_skew(corrected)
            print(f"→ New skew angle: {new_angle:.2f}")
            skew_angles[i] = new_angle
    return numpy_images

# ──────────────────────────────────────────────
# Full alignment pipeline
def auto_align_pages(pdf_path: str):
    skew_angles, numpy_images, pil_images = find_all_page_rotation(pdf_path)
    
    # Find misaligned pages
    misaligned = [(i, angle) for i, angle in enumerate(skew_angles) if abs(angle) > 0.5]
    if not misaligned:
        print("✅ All pages are already aligned.")
        return numpy_images
    
    print("⚠️ Misaligned pages found:", misaligned)
    
    # Deskew
    corrected_images = deskew_misaligned_pages(skew_angles, numpy_images)
    return corrected_images

# ──────────────────────────────────────────────
# Example usage
if __name__ == "__main__":
    pdf_path = r'D:\Projects\Intelligent Document Processing\sample_data\pdf\sample_pdf.pdf'
    
    corrected_images = auto_align_pages(pdf_path)

    # Optional: Save corrected images to files
    for i, img in enumerate(corrected_images):
        output_path = f"corrected_page_{i + 1}.png"
        cv2.imwrite(output_path, img)
        print(f"✅ Saved: {output_path}")
