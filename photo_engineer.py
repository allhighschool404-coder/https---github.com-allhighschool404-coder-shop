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
            # 'u2net_human_seg' is the specialized human portrait segmentation model
            # with pin-sharp precision on hair, ears, badges, and shoulders (~1.5s on CPU)
            _REMBG_SESSION = rembg.new_session('u2net_human_seg')
        except Exception as e:
            try:
                import rembg
                _REMBG_SESSION = rembg.new_session('u2netp')
            except Exception as e2:
                try:
                    import rembg
                    _REMBG_SESSION = rembg.new_session('silueta')
                except Exception as e3:
                    print(f"Warning: Could not initialize rembg session: {e3}")
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
    Remove background using rembg (u2net_human_seg).
    Ensures clean background separation without dark halos around ears or shoulders.
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

            # Remove background using human_seg session
            rgba_out = rembg.remove(work_img, session=session)

            # Restore original dimensions if scaled
            if rgba_out.size != (orig_w, orig_h):
                rgba_out = rgba_out.resize((orig_w, orig_h), Image.Resampling.LANCZOS)

            # Clean alpha thresholding to eliminate background haze and dark halos
            r, g, b, a = rgba_out.split()
            a_arr = np.array(a)
            # Threshold noise: values below 12 become 0 (pure transparent)
            a_arr[a_arr < 12] = 0
            # Solidify confident foreground: values above 242 become 255 (solid)
            a_arr[a_arr > 242] = 255
            clean_a = Image.fromarray(a_arr)
            return Image.merge('RGBA', (r, g, b, clean_a))
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
    Subtle, studio-quality photo fresh enhancer.
    Guarantees 100% preservation of genuine facial features, skin pores, and natural likeness.
    """
    img_rgb = np.array(pil_img.convert('RGB'))

    eff_brightness = brightness
    eff_contrast = contrast
    eff_smoothness = smoothness
    eff_sharpness = sharpness
    eff_saturation = saturation

    # If auto_fresh, set gentle studio enhancement defaults (without harsh plastic distortion)
    if auto_fresh:
        if eff_brightness == 0: eff_brightness = 4
        if eff_contrast == 0: eff_contrast = 6
        if eff_sharpness == 0: eff_sharpness = 16
        if eff_saturation == 0: eff_saturation = 5
        # Do NOT apply heavy smoothness by default so authentic skin pores and face structure are 100% preserved
        if eff_smoothness == 0: eff_smoothness = 0

    # 1. Optical deblurring for genuinely blurry / out of focus photos
    if auto_fresh:
        try:
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            blur_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if blur_var < 160.0: # blurry/fuzzy photo
                blurred = cv2.GaussianBlur(img_rgb, (0, 0), sigmaX=1.8)
                img_rgb = cv2.addWeighted(img_rgb, 1.35, blurred, -0.35, 0)
                img_rgb = np.clip(img_rgb, 0, 255).astype(np.uint8)
        except Exception as e:
            print(f"Deblur error: {e}")

    # 2. Skin Smoothing (Bilateral Filter) only if explicitly requested
    if eff_smoothness > 0:
        try:
            ratio = max(0.0, min(float(eff_smoothness) / 100.0, 1.0))
            sigma = int(15 + ratio * 35)
            filtered = cv2.bilateralFilter(img_rgb, d=5, sigmaColor=sigma, sigmaSpace=sigma)
            img_rgb = cv2.addWeighted(filtered, ratio * 0.7, img_rgb, 1.0 - (ratio * 0.7), 0)
        except Exception as e:
            print(f"Smoothness error: {e}")

    enhanced_pil = Image.fromarray(img_rgb)

    # 3. Brightness adjustment
    if eff_brightness != 0:
        factor = 1.0 + (eff_brightness / 100.0) * 0.5
        enhanced_pil = ImageEnhance.Brightness(enhanced_pil).enhance(max(0.2, factor))

    # 4. Contrast adjustment
    if eff_contrast != 0:
        factor = 1.0 + (eff_contrast / 100.0) * 0.5
        enhanced_pil = ImageEnhance.Contrast(enhanced_pil).enhance(max(0.2, factor))

    # 5. Color Saturation / Warmth
    if eff_saturation != 0:
        factor = 1.0 + (eff_saturation / 100.0) * 0.4
        enhanced_pil = ImageEnhance.Color(enhanced_pil).enhance(max(0.1, factor))

    # 6. Crisp Studio Sharpness
    if eff_sharpness > 0:
        factor = 1.0 + (eff_sharpness / 100.0) * 0.8
        enhanced_pil = ImageEnhance.Sharpness(enhanced_pil).enhance(factor)

    return enhanced_pil

def detect_head_and_shoulders_crop(subject_rgba, target_aspect_ratio=0.8):
    """
    Intelligently crops full-body photos to upper body:
    - Only triggers on TRUE standing full-body photos (person_h > person_w * 2.1).
    - Preserves full natural shoulder width and badges without clipping.
    - If already a portrait, bust, or half-body photo, preserves natural bounds 100%.
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
        orig_w, orig_h = subject_rgba.size

        # Only crop if it is a TRUE full-body photo (head-to-toe standing, ratio > 2.1)
        if person_h > person_w * 2.1 and person_h > 500:
            head_h_est = int(person_h * 0.16)
            crop_bottom = min(orig_h, min_y + int(head_h_est * 3.2))
            # Keep full width so shoulders and badges are never cut off
            return subject_rgba.crop((0, min_y, orig_w, crop_bottom))
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
    1. Background removal first (on pristine image)
    2. Fresh Studio Enhancement on the subject
    3. Smart Head & Shoulders framing for official passport/ID/office use
    4. Studio placement with comfortable shoulder margins and proper headroom
    """
    # 1. Background Processing first (on pristine image)
    if remove_bg:
        subject_rgba = remove_bg_ai(pil_img)
    else:
        subject_rgba = pil_img.convert('RGBA')

    # 2. Fresh Studio Enhancement on the subject
    r, g, b, a = subject_rgba.split()
    rgb_part = Image.merge('RGB', (r, g, b))
    fresh_rgb = enhance_photo(
        rgb_part,
        brightness=brightness,
        contrast=contrast,
        smoothness=smoothness,
        sharpness=sharpness,
        saturation=saturation,
        auto_fresh=auto_fresh
    )
    r2, g2, b2 = fresh_rgb.split()
    subject_rgba = Image.merge('RGBA', (r2, g2, b2, a))

    # 3. Smart Framing for full-body photos (if applicable)
    aspect_ratio = target_w / float(target_h)
    framed_subject = detect_head_and_shoulders_crop(subject_rgba, target_aspect_ratio=aspect_ratio)

    # 4. Measure subject bounding box
    alpha = np.array(framed_subject.split()[-1])
    ys, xs = np.where(alpha > 25)
    if len(ys) == 0:
        if bg_color is not None:
            return Image.new('RGB', (target_w, target_h), bg_color)
        return Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

    person_w = int(xs.max() - xs.min())
    person_h = int(ys.max() - ys.min())

    # Studio Passport / Portrait Composition:
    # In portrait: shoulders occupy ~88% of target_w, headroom ~8%
    # In landscape: shoulders occupy ~65% of target_w, headroom ~10%
    is_portrait = target_h >= target_w
    if is_portrait:
        target_subject_w = target_w * 0.88
        headroom_ratio = 0.08
    else:
        target_subject_w = target_w * 0.65
        headroom_ratio = 0.10

    # Scale uniformly (LANCZOS) with user's zoom factor (crop_scale)
    scale = (target_subject_w / float(max(1, person_w))) * float(crop_scale)
    new_w = max(1, int(round(framed_subject.width * scale)))
    new_h = max(1, int(round(framed_subject.height * scale)))

    scaled_sub = framed_subject.resize((new_w, new_h), Image.Resampling.LANCZOS)
    scaled_alpha = np.array(scaled_sub.split()[-1])
    sc_ys, sc_xs = np.where(scaled_alpha > 25)

    if len(sc_ys) == 0:
        if bg_color is not None:
            return Image.new('RGB', (target_w, target_h), bg_color)
        return Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

    sc_min_y = int(sc_ys.min())
    sc_min_x, sc_max_x = int(sc_xs.min()), int(sc_xs.max())
    sc_center_x = (sc_min_x + sc_max_x) // 2

    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    desired_head_top = int(target_h * headroom_ratio)

    pos_y = desired_head_top - sc_min_y + int(pan_y * target_h / 100.0)
    pos_x = (target_w // 2) - sc_center_x + int(pan_x * target_w / 100.0)

    canvas.paste(scaled_sub, (pos_x, pos_y), scaled_sub)

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
        joint_aspect = (target_w * 0.52) / float(target_h)
        sub1_rgba = detect_head_and_shoulders_crop(sub1_rgba, target_aspect_ratio=joint_aspect)
        sub2_rgba = detect_head_and_shoulders_crop(sub2_rgba, target_aspect_ratio=joint_aspect)

        canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))

        # Each person takes ~52% width of the frame so they stand side-by-side naturally
        target_sub_w = int(target_w * 0.52)

        # Scale person 1
        s1_alpha = np.array(sub1_rgba.split()[-1])
        s1_ys, s1_xs = np.where(s1_alpha > 25)
        p1_w_actual = (s1_xs.max() - s1_xs.min()) if len(s1_xs) > 0 else sub1_rgba.width
        scale_val1 = (target_sub_w / float(max(1, p1_w_actual))) * scale1
        p1_w = int(round(sub1_rgba.width * scale_val1))
        p1_h = int(round(sub1_rgba.height * scale_val1))
        p1_resized = sub1_rgba.resize((p1_w, p1_h), Image.Resampling.LANCZOS)

        # Scale person 2
        s2_alpha = np.array(sub2_rgba.split()[-1])
        s2_ys, s2_xs = np.where(s2_alpha > 25)
        p2_w_actual = (s2_xs.max() - s2_xs.min()) if len(s2_xs) > 0 else sub2_rgba.width
        scale_val2 = (target_sub_w / float(max(1, p2_w_actual))) * scale2
        p2_w = int(round(sub2_rgba.width * scale_val2))
        p2_h = int(round(sub2_rgba.height * scale_val2))
        p2_resized = sub2_rgba.resize((p2_w, p2_h), Image.Resampling.LANCZOS)

        headroom = int(target_h * 0.08)
        p1_top_arr = np.where(np.array(p1_resized.split()[-1]) > 25)[0]
        p1_head_y = int(p1_top_arr.min()) if len(p1_top_arr) > 0 else 0

        p2_top_arr = np.where(np.array(p2_resized.split()[-1]) > 25)[0]
        p2_head_y = int(p2_top_arr.min()) if len(p2_top_arr) > 0 else 0

        # Position person 1 (left side ~28%) and person 2 (right side ~72%)
        p1_x = int(round((target_w * 0.28) - (p1_w / 2.0) + (pos_x1 * target_w / 100.0) - (gap / 2.0)))
        p1_y = headroom - p1_head_y

        p2_x = int(round((target_w * 0.72) - (p2_w / 2.0) + (pos_x2 * target_w / 100.0) + (gap / 2.0)))
        p2_y = headroom - p2_head_y

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

