import io
import math
import base64
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

# Lazy-loaded rembg session
_REMBG_SESSION = None

def get_rembg_session():
    global _REMBG_SESSION
    if _REMBG_SESSION is None:
        try:
            import rembg
            # 'silueta' is lightweight (~44MB), fast (1s on CPU), and optimized for human portraits
            _REMBG_SESSION = rembg.new_session('silueta')
        except Exception as e:
            try:
                import rembg
                _REMBG_SESSION = rembg.new_session('u2netp')
            except Exception as e2:
                print(f"Warning: Could not initialize rembg session: {e2}")
                _REMBG_SESSION = False
    return _REMBG_SESSION if _REMBG_SESSION is not False else None

# Predefined sizes in pixels at 300 DPI
PRESET_SIZES = {
    # 40mm x 50mm (Bangladesh standard passport)
    'passport_bd': {'name': 'পাসপোর্ট (বাংলাদেশ) - ৪০x৫০ মিমি', 'w_mm': 40, 'h_mm': 50, 'w_px': 472, 'h_px': 591},
    # 35mm x 45mm (International / Biometric / Schengen passport)
    'passport_intl': {'name': 'পাসপোর্ট (আন্তর্জাতিক) - ৩৫x৪৫ মিমি', 'w_mm': 35, 'h_mm': 45, 'w_px': 413, 'h_px': 531},
    # 2 x 2 inch (50.8mm x 50.8mm - US / India / Visa)
    'passport_us': {'name': 'ভিসা / ২x২ ইঞ্চি - ৫০.৮x৫০.৮ মিমি', 'w_mm': 50.8, 'h_mm': 50.8, 'w_px': 600, 'h_px': 600},
    # 20mm x 25mm (Stamp size)
    'stamp': {'name': 'স্ট্যাম্প সাইজ - ২০x২৫ মিমি', 'w_mm': 20, 'h_mm': 25, 'w_px': 236, 'h_px': 295},
    # 3R size (3.5 x 5 inch)
    '3r': {'name': '৩-আর (3R) সাইজ - ৩.৫x৫.০ ইঞ্চি', 'w_mm': 88.9, 'h_mm': 127.0, 'w_px': 1050, 'h_px': 1500},
    # 4R size (4 x 6 inch)
    '4r': {'name': '৪-আর (4R) সাইজ - ৪.০x৬.০ ইঞ্চি', 'w_mm': 101.6, 'h_mm': 152.4, 'w_px': 1200, 'h_px': 1800},
    # 10R size (10 x 12 inch)
    '10r': {'name': '১০-আর (10R) সাইজ - ১০.০x১২.০ ইঞ্চি', 'w_mm': 254.0, 'h_mm': 304.8, 'w_px': 3000, 'h_px': 3600},
}

# Standard Studio Colors (Hex and RGB)
STUDIO_COLORS = {
    'studio_blue': {'name': 'স্টুডিও ক্লাসিক ব্লু', 'hex': '#1E6091', 'rgb': (30, 96, 145)},
    'royal_blue': {'name': 'রয়েল ব্লু', 'hex': '#0047AB', 'rgb': (0, 71, 171)},
    'vivid_blue': {'name': 'উজ্জ্বল ব্লু', 'hex': '#2B78E4', 'rgb': (43, 120, 228)},
    'sky_blue': {'name': 'আকাশি ব্লু', 'hex': '#85C1E9', 'rgb': (133, 193, 233)},
    'white': {'name': 'সাদা (অফিশিয়াল/ভিসা)', 'hex': '#FFFFFF', 'rgb': (255, 255, 255)},
    'light_gray': {'name': 'হালকা ধূসর', 'hex': '#E5E7EB', 'rgb': (229, 231, 235)},
    'red': {'name': 'লাল (রেড ব্যাকগ্রাউন্ড)', 'hex': '#C0392B', 'rgb': (192, 57, 43)},
}

def hex_to_rgb(hex_str):
    """Convert hex color string like #1E6091 to (R, G, B) tuple."""
    if not hex_str:
        return (30, 96, 145) # default studio blue
    hex_str = hex_str.strip().lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    if len(hex_str) >= 6:
        try:
            return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
        except ValueError:
            pass
    return (30, 96, 145)

def get_dimensions(size_preset, orientation='portrait', custom_w=None, custom_h=None, custom_unit='mm'):
    """Return width and height in pixels at 300 DPI."""
    if size_preset == 'custom' and custom_w and custom_h:
        try:
            w_val = float(custom_w)
            h_val = float(custom_h)
            if custom_unit == 'mm':
                w_px = int(round((w_val / 25.4) * 300))
                h_px = int(round((h_val / 25.4) * 300))
            elif custom_unit == 'in':
                w_px = int(round(w_val * 300))
                h_px = int(round(h_val * 300))
            else: # px
                w_px = int(round(w_val))
                h_px = int(round(h_val))
        except (ValueError, TypeError):
            w_px, h_px = 472, 591
    elif size_preset in PRESET_SIZES:
        p = PRESET_SIZES[size_preset]
        w_px, h_px = p['w_px'], p['h_px']
    else:
        w_px, h_px = 472, 591 # default BD passport

    # Adjust for orientation
    if orientation == 'landscape':
        if w_px < h_px:
            w_px, h_px = h_px, w_px
    else: # portrait
        if w_px > h_px:
            w_px, h_px = h_px, w_px

    # Bound size between 100px and 6000px
    w_px = max(100, min(w_px, 6000))
    h_px = max(100, min(h_px, 6000))
    return w_px, h_px

def remove_bg_ai(pil_img):
    """
    Remove background using rembg (silueta or u2netp).
    Includes edge feathering for smooth hair and shoulder contours.
    """
    orig_w, orig_h = pil_img.size
    session = get_rembg_session()

    if session is not None:
        try:
            import rembg
            # Downsample temporarily if image is gigantic for speed
            max_dim = max(orig_w, orig_h)
            if max_dim > 1600:
                scale = 1600.0 / max_dim
                work_img = pil_img.resize((int(round(orig_w * scale)), int(round(orig_h * scale))), Image.Resampling.LANCZOS)
            else:
                work_img = pil_img

            # Remove background
            rgba_out = rembg.remove(work_img, session=session)

            # Restore original dimensions if scaled
            if rgba_out.size != (orig_w, orig_h):
                rgba_out = rgba_out.resize((orig_w, orig_h), Image.Resampling.LANCZOS)

            # Smooth alpha mask edges slightly to eliminate jagged edge artifacts
            r, g, b, a = rgba_out.split()
            # Slight Gaussian blur on alpha channel
            a_blurred = a.filter(ImageFilter.GaussianBlur(radius=0.7))
            rgba_out = Image.merge('RGBA', (r, g, b, a_blurred))
            return rgba_out
        except Exception as e:
            print(f"Error in rembg execution: {e}")

    # Fallback if rembg is not available or failed: Smart GrabCut / skin segmentation fallback
    return fallback_remove_bg(pil_img)

def fallback_remove_bg(pil_img):
    """
    OpenCV GrabCut fallback for background removal.
    Assumes center rectangular region is the subject.
    """
    try:
        cv_img = cv2.cvtColor(np.array(pil_img.convert('RGB')), cv2.COLOR_RGB2BGR)
        h, w = cv_img.shape[:2]
        
        mask = np.zeros((h, w), np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        
        # Center margin 5%
        rect = (int(w * 0.05), int(h * 0.05), int(w * 0.90), int(h * 0.90))
        cv2.grabCut(cv_img, mask, rect, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_RECT)
        
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        # Soften mask
        mask2 = (mask2 * 255).astype(np.uint8)
        mask2 = cv2.GaussianBlur(mask2, (5, 5), 0)
        
        rgba = pil_img.convert('RGBA')
        r, g, b, _ = rgba.split()
        alpha = Image.fromarray(mask2)
        return Image.merge('RGBA', (r, g, b, alpha))
    except Exception as e:
        print(f"GrabCut fallback failed: {e}")
        return pil_img.convert('RGBA')

def enhance_photo(pil_img, brightness=0, contrast=0, smoothness=0, sharpness=0, saturation=0, auto_fresh=True):
    """
    Photo Fresh Studio Enhancer:
    - Auto Fresh: Intelligently balances light (CLAHE), softens skin, enhances sharpness and skin vibrance.
    - Bilateral / Edge-Preserving smoothing: smoothens skin blemish and noise while preserving crisp facial features.
    - Unsharp mask: studio portrait sharpness.
    - Exposure and color vibrance adjustments.
    """
    # Convert PIL Image to RGB numpy array
    img_rgb = np.array(pil_img.convert('RGB'))

    # If Auto Fresh is requested and user didn't manually customize or wanted auto defaults
    if auto_fresh:
        if brightness == 0: brightness = 8
        if contrast == 0: contrast = 12
        if smoothness == 0: smoothness = 30
        if sharpness == 0: sharpness = 28
        if saturation == 0: saturation = 10

    # 0. Optical deblurring & sharpness restoration for blurry/unclear input photos
    if auto_fresh:
        try:
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            blur_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            # If photo is blurry or out of focus (Laplacian variance < 200), apply optical deblur
            if blur_var < 200.0:
                gaussian_blur = cv2.GaussianBlur(img_rgb, (0, 0), sigmaX=2.0)
                # True optical unsharp recovery: sharpens real edges without distorting facial geometry
                img_rgb = cv2.addWeighted(img_rgb, 1.45, gaussian_blur, -0.45, 0)
                img_rgb = np.clip(img_rgb, 0, 255).astype(np.uint8)
        except Exception as e:
            print(f"Deblur error: {e}")

    # 1. CLAHE exposure balance on L-channel if auto_fresh
    if auto_fresh:
        try:
            lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge((l, a, b))
            img_rgb = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        except Exception as e:
            print(f"CLAHE error: {e}")

    # 2. Skin Smoothing (Bilateral Filter / Edge Preserving Filter)
    if smoothness > 0:
        try:
            smooth_ratio = max(0.0, min(float(smoothness) / 100.0, 1.0))
            # d: diameter of filter, sigmaColor: color difference tolerance, sigmaSpace: spatial distance
            sigma = int(25 + smooth_ratio * 55)
            filtered = cv2.bilateralFilter(img_rgb, d=7, sigmaColor=sigma, sigmaSpace=sigma)
            # Blend original and filtered based on smoothness ratio
            img_rgb = cv2.addWeighted(filtered, smooth_ratio, img_rgb, 1.0 - smooth_ratio, 0)
        except Exception as e:
            print(f"Smoothness error: {e}")

    # Convert back to PIL for high-quality tone & color enhancements
    enhanced_pil = Image.fromarray(img_rgb)

    # 3. Brightness adjustment (-100 to 100 -> factor 0.0 to 2.0)
    if brightness != 0:
        factor = 1.0 + (brightness / 100.0) * 0.6
        enhanced_pil = ImageEnhance.Brightness(enhanced_pil).enhance(max(0.1, factor))

    # 4. Contrast adjustment (-100 to 100 -> factor 0.0 to 2.0)
    if contrast != 0:
        factor = 1.0 + (contrast / 100.0) * 0.6
        enhanced_pil = ImageEnhance.Contrast(enhanced_pil).enhance(max(0.1, factor))

    # 5. Color Saturation / Warmth (-100 to 100 -> factor 0.0 to 2.0)
    if saturation != 0:
        factor = 1.0 + (saturation / 100.0) * 0.5
        enhanced_pil = ImageEnhance.Color(enhanced_pil).enhance(max(0.0, factor))

    # 6. Sharpness (Unsharp Masking) (0 to 100)
    if sharpness > 0:
        sharp_factor = 1.0 + (sharpness / 100.0) * 1.5
        enhanced_pil = ImageEnhance.Sharpness(enhanced_pil).enhance(sharp_factor)

    return enhanced_pil

def detect_head_and_shoulders_crop(subject_rgba, target_aspect_ratio=0.8):
    """
    Intelligently crops full-body or half-body photos to head & shoulders:
    - Analyzes alpha mask to find person bounds.
    - If person is full-body or tall (person_h > person_w * 1.25),
      identifies head and neck/shoulder expansion.
    - Crops head and upper chest with standard official passport headroom (8-10%)
      and 65-75% face height ratio.
    - If already a portrait or close-up, preserves natural bounds.
    - Strictly preserves authentic aspect ratio and face geometry (zero distortion).
    """
    try:
        alpha = np.array(subject_rgba.split()[-1])
        y_idx, x_idx = np.where(alpha > 25)
        if len(y_idx) == 0:
            return subject_rgba

        min_y, max_y = int(y_idx.min()), int(y_idx.max())
        min_x, max_x = int(x_idx.min()), int(x_idx.max())
        person_h = max_y - min_y
        person_w = max_x - min_x

        # If image is a full-body or half-body photo (tall person ratio)
        if person_h > person_w * 1.25 and person_h > 200:
            # Sample widths from top of head downwards
            step = max(1, person_h // 80)
            widths = []
            for y in range(min_y, min(max_y, min_y + int(person_h * 0.45)), step):
                row_x = np.where(alpha[y, :] > 25)[0]
                w = (row_x.max() - row_x.min()) if len(row_x) > 0 else 0
                widths.append((y, w))

            # Detect neck-to-shoulder transition (where width expands)
            shoulder_y = None
            if len(widths) > 5:
                head_w_samples = [w for y, w in widths[:len(widths)//3] if w > 0]
                if head_w_samples:
                    med_hw = np.median(head_w_samples)
                    for y, w in widths:
                        if y > min_y + int(person_h * 0.10) and w > med_hw * 1.45:
                            shoulder_y = y
                            break

            if not shoulder_y:
                shoulder_y = min_y + int(person_h * 0.28)

            head_h = max(40, shoulder_y - min_y)

            # Official passport framing: include headroom and upper chest/shoulders
            crop_top = max(0, min_y - int(head_h * 0.15))
            crop_bottom = min(subject_rgba.height, min_y + int(head_h * 2.35))
            crop_h = crop_bottom - crop_top

            # Center X around the head
            head_alpha = alpha[min_y:shoulder_y, :]
            h_y, h_x = np.where(head_alpha > 25)
            center_x = int(np.median(h_x)) if len(h_x) > 0 else (min_x + max_x) // 2

            crop_w = int(crop_h * target_aspect_ratio)
            crop_left = max(0, center_x - crop_w // 2)
            crop_right = min(subject_rgba.width, crop_left + crop_w)

            if crop_right - crop_left < crop_w:
                crop_left = max(0, crop_right - crop_w)

            return subject_rgba.crop((crop_left, crop_top, crop_right, crop_bottom))
    except Exception as e:
        print(f"Smart framing error: {e}")

    return subject_rgba

def fit_and_compose_single(
    pil_img,
    target_w,
    target_h,
    bg_color=(30, 96, 145),
    remove_bg=True,
    auto_fresh=True,
    brightness=0,
    contrast=0,
    smoothness=0,
    sharpness=0,
    saturation=0,
    crop_scale=1.0,
    pan_x=0,
    pan_y=0
):
    """
    Process single photo:
    1. Fresh Studio Enhancement with Deblur
    2. Remove background and composite onto chosen Studio Blue / custom color
    3. Smart Head & Shoulders framing for official passport/ID/office use
    4. Fit and center nicely inside target canvas (Passport, Stamp, 3R, 4R, 10R)
    """
    # 1. Photo Fresh & Deblur
    fresh_img = enhance_photo(
        pil_img,
        brightness=brightness,
        contrast=contrast,
        smoothness=smoothness,
        sharpness=sharpness,
        saturation=saturation,
        auto_fresh=auto_fresh
    )

    # 2. Background Processing
    if remove_bg:
        subject_rgba = remove_bg_ai(fresh_img)
    else:
        subject_rgba = fresh_img.convert('RGBA')

    # 3. Smart Face & Upper Torso Framing for office/passport standard
    aspect_ratio = target_w / float(target_h)
    framed_subject = detect_head_and_shoulders_crop(subject_rgba, target_aspect_ratio=aspect_ratio)

    # 4. Framing / Composition into target dimensions (target_w, target_h)
    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

    sub_w, sub_h = framed_subject.size

    # Calculate scale to cover canvas appropriately (standard portrait framing)
    scale_w = target_w / float(sub_w)
    scale_h = target_h / float(sub_h)
    base_scale = max(scale_w, scale_h) * crop_scale

    new_w = int(round(sub_w * base_scale))
    new_h = int(round(sub_h * base_scale))
    resized_subject = framed_subject.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Position with pan offsets (default centered)
    offset_x = int(round((target_w - new_w) / 2.0 + (pan_x * target_w / 100.0)))
    offset_y = int(round((target_h - new_h) / 2.0 + (pan_y * target_h / 100.0)))

    # Paste onto canvas
    canvas.paste(resized_subject, (offset_x, offset_y), resized_subject)

    # 5. Apply background color if not transparent
    if bg_color is not None:
        bg = Image.new('RGBA', (target_w, target_h), bg_color + (255,))
        final_img = Image.alpha_composite(bg, canvas).convert('RGB')
        return final_img
    else:
        return canvas

def compose_dual_photos(
    pil_img1,
    pil_img2,
    target_w,
    target_h,
    layout='joint', # 'joint' (unified studio frame) or 'side_by_side' (split)
    bg_color=(30, 96, 145),
    remove_bg=True,
    auto_fresh=True,
    brightness=0,
    contrast=0,
    smoothness=0,
    sharpness=0,
    saturation=0,
    scale1=1.0,
    pos_x1=0,
    scale2=1.0,
    pos_x2=0,
    gap=0
):
    """
    Dual / Joint Photo Combination:
    - 'joint': Unified couple/two-person portrait on matching studio background.
    - 'side_by_side': Split photo (left & right halves) with clean separator.
    """
    # 1. Fresh Enhancement for both
    fresh1 = enhance_photo(pil_img1, brightness, contrast, smoothness, sharpness, saturation, auto_fresh)
    fresh2 = enhance_photo(pil_img2, brightness, contrast, smoothness, sharpness, saturation, auto_fresh)

    # 2. Background removal for both
    if remove_bg:
        sub1_rgba = remove_bg_ai(fresh1)
        sub2_rgba = remove_bg_ai(fresh2)
    else:
        sub1_rgba = fresh1.convert('RGBA')
        sub2_rgba = fresh2.convert('RGBA')

    if layout == 'side_by_side':
        # Split target_w into two equal halves with gap in between
        half_w = (target_w - gap) // 2
        half_h = target_h

        img1_half = fit_and_compose_single(
            pil_img1, half_w, half_h, bg_color=None,
            remove_bg=remove_bg, auto_fresh=auto_fresh,
            brightness=brightness, contrast=contrast, smoothness=smoothness,
            sharpness=sharpness, saturation=saturation, crop_scale=scale1
        )
        img2_half = fit_and_compose_single(
            pil_img2, half_w, half_h, bg_color=None,
            remove_bg=remove_bg, auto_fresh=auto_fresh,
            brightness=brightness, contrast=contrast, smoothness=smoothness,
            sharpness=sharpness, saturation=saturation, crop_scale=scale2
        )

        canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
        canvas.paste(img1_half, (0, 0), img1_half)
        canvas.paste(img2_half, (half_w + gap, 0), img2_half)

        # Draw a sleek subtle divider line if gap > 0 or default white hairline
        if gap > 0:
            divider = Image.new('RGBA', (gap, target_h), (255, 255, 255, 255))
            canvas.paste(divider, (half_w, 0))

        if bg_color is not None:
            bg = Image.new('RGBA', (target_w, target_h), bg_color + (255,))
            return Image.alpha_composite(bg, canvas).convert('RGB')
        return canvas

    else: # 'joint' unified portrait
        # Smart head-and-shoulders framing for both subjects so full-body inputs are neatly balanced
        joint_aspect = (target_w * 0.58) / float(target_h)
        sub1_rgba = detect_head_and_shoulders_crop(sub1_rgba, target_aspect_ratio=joint_aspect)
        sub2_rgba = detect_head_and_shoulders_crop(sub2_rgba, target_aspect_ratio=joint_aspect)

        canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

        # Size estimation: each person takes roughly 55-60% width of the frame so they overlap/stand naturally
        target_sub_w = int(target_w * 0.58)

        # Scale person 1
        s1_w, s1_h = sub1_rgba.size
        scale_val1 = (target_sub_w / float(s1_w)) * scale1
        p1_w = int(round(s1_w * scale_val1))
        p1_h = int(round(s1_h * scale_val1))
        p1_resized = sub1_rgba.resize((p1_w, p1_h), Image.Resampling.LANCZOS)

        # Scale person 2
        s2_w, s2_h = sub2_rgba.size
        scale_val2 = (target_sub_w / float(s2_w)) * scale2
        p2_w = int(round(s2_w * scale_val2))
        p2_h = int(round(s2_h * scale_val2))
        p2_resized = sub2_rgba.resize((p2_w, p2_h), Image.Resampling.LANCZOS)

        # Position person 1 (left side) and person 2 (right side)
        # Baseline y is aligned towards the bottom of the photo
        p1_x = int(round((target_w * 0.25) - (p1_w / 2.0) + (pos_x1 * target_w / 100.0) - (gap / 2.0)))
        p1_y = target_h - p1_h

        p2_x = int(round((target_w * 0.75) - (p2_w / 2.0) + (pos_x2 * target_w / 100.0) + (gap / 2.0)))
        p2_y = target_h - p2_h

        # Paste person 1 and person 2
        canvas.paste(p1_resized, (p1_x, p1_y), p1_resized)
        canvas.paste(p2_resized, (p2_x, p2_y), p2_resized)

        if bg_color is not None:
            bg = Image.new('RGBA', (target_w, target_h), bg_color + (255,))
            return Image.alpha_composite(bg, canvas).convert('RGB')
        return canvas

def make_print_sheet(photo_img, sheet_size='4r', layout_type='passport_grid', border=True):
    """
    Generate studio print sheet (4R or A4) at 300 DPI:
    - 4R (4 x 6 inch / 1200 x 1800 px)
    - A4 (210 x 297 mm / 2480 x 3508 px)
    Tiles multiple copies neatly with cutting guide lines!
    """
    photo_rgb = photo_img.convert('RGB')
    pw, ph = photo_rgb.size

    if sheet_size == 'a4':
        sheet_w, sheet_h = 2480, 3508 # A4 portrait
    else: # 4r
        sheet_w, sheet_h = 1800, 1200 # 4R landscape (standard photo paper tray)

    sheet = Image.new('RGB', (sheet_w, sheet_h), (255, 255, 255))
    
    # Calculate how many photos fit
    # Let's add slight margin and cutting guide border
    margin = 50
    spacing = 30

    # Auto calculate grid
    cols = max(1, (sheet_w - 2 * margin + spacing) // (pw + spacing))
    rows = max(1, (sheet_h - 2 * margin + spacing) // (ph + spacing))

    # Center the entire grid
    total_grid_w = cols * pw + (cols - 1) * spacing
    total_grid_h = rows * ph + (rows - 1) * spacing
    start_x = (sheet_w - total_grid_w) // 2
    start_y = (sheet_h - total_grid_h) // 2

    # Draw border around each photo if requested
    bordered_photo = photo_rgb.copy()
    if border:
        # Faint gray 1px cutting border
        bordered_photo = ImageOps.expand(bordered_photo, border=2, fill=(210, 210, 210))
        bw, bh = bordered_photo.size
    else:
        bw, bh = pw, ph

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (pw + spacing)
            y = start_y + r * (ph + spacing)
            sheet.paste(bordered_photo, (x, y))

    return sheet

