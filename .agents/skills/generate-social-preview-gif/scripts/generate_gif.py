"""
Generate Social Preview GIF (640x320px, <1MB, 50px top/bottom padding)
Matching the Awesome Public Health Surveillance banner styling.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH = 640
HEIGHT = 320
TOP_PADDING = 50
BOTTOM_PADDING = 50
CONTENT_TOP = TOP_PADDING
CONTENT_BOTTOM = HEIGHT - BOTTOM_PADDING  # 270

TOTAL_FRAMES = 30
FPS = 20
DURATION_MS = int(1000 / FPS)

# Font loading helper
def get_fonts():
    font_paths_bold = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_paths_reg = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    font_title = None
    font_sub = None
    font_badge = None
    font_tag = None

    for p in font_paths_bold:
        if os.path.exists(p):
            font_title = ImageFont.truetype(p, 23)
            font_badge = ImageFont.truetype(p, 10)
            break
            
    for p in font_paths_reg:
        if os.path.exists(p):
            font_sub = ImageFont.truetype(p, 12)
            font_tag = ImageFont.truetype(p, 11)
            break

    if not font_title:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    return font_title, font_sub, font_badge, font_tag

def create_base_background():
    """Create background gradient with dark medical/tech tones."""
    base = Image.new("RGBA", (WIDTH, HEIGHT))
    # Diagonal/vertical gradient from #0f172a (15,23,42) to #1e1b4b (30,27,75)
    c1 = np.array([15, 23, 42], dtype=float)
    c2 = np.array([30, 27, 75], dtype=float)
    
    arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        ratio_y = y / float(HEIGHT)
        for x in range(WIDTH):
            ratio_x = x / float(WIDTH)
            blend = (ratio_y * 0.7 + ratio_x * 0.3)
            color = (1.0 - blend) * c1 + blend * c2
            arr[y, x] = color.astype(np.uint8)
            
    base = Image.fromarray(arr).convert("RGBA")
    draw = ImageDraw.Draw(base)

    # Draw grid lines
    grid_color = (51, 65, 85, 45)  # #334155 with alpha
    for x in range(40, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(30, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

    # Border stroke
    draw.rounded_rectangle([(1, 1), (WIDTH - 2, HEIGHT - 2)], radius=12, outline=(51, 65, 85, 120), width=2)
    return base

def render_frame(frame_idx, base_bg, fonts):
    font_title, font_sub, font_badge, font_tag = fonts
    frame = base_bg.copy()
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    t = frame_idx / float(TOTAL_FRAMES)  # 0.0 to 1.0
    phase = 2 * math.pi * t

    # 1. Floating Pill Badge (inside safe area: y=56 to 82)
    badge_x = 40
    badge_y = 56 + int(2 * math.sin(phase))
    badge_w = 215
    badge_h = 24
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=12,
        fill=(30, 41, 59, 230),
        outline=(2, 132, 199, 220),
        width=1
    )
    
    # Blinking green surveillance indicator dot
    pulse_alpha = int(140 + 115 * math.sin(phase * 2))
    dot_radius = 4
    dot_cx = badge_x + 14
    dot_cy = badge_y + 12
    draw.ellipse(
        [(dot_cx - dot_radius, dot_cy - dot_radius), (dot_cx + dot_radius, dot_cy + dot_radius)],
        fill=(16, 185, 129, pulse_alpha)
    )
    draw.text((badge_x + 26, badge_y + 6), "GLOBAL HEALTH INTELLIGENCE", font=font_badge, fill=(56, 189, 248, 255))

    # 2. Main Title (within y=88 to 118)
    draw.text((40, 88), "Awesome Public Health Surveillance", font=font_title, fill=(255, 255, 255, 255))

    # 3. Subtitle (within y=118 to 138)
    draw.text(
        (40, 118),
        "Curated SaaS Platforms, DHIS2, Outbreak Response & Epi Analytics",
        font=font_sub,
        fill=(148, 163, 184, 255)
    )

    # 4. Animated Surveillance Signal / Waveform
    # Spans across y=165 to 205 (content zone)
    baseline_y = 180
    wave_pts = []
    glow_pts = []
    
    step_x = 4
    for x in range(20, WIDTH - 20 + step_x, step_x):
        # Combined harmonic wave with moving phase
        y_offset = (
            18.0 * math.sin(2 * math.pi * x / 240.0 - phase)
            + 9.0 * math.sin(2 * math.pi * x / 110.0 + phase * 1.5)
            + 5.0 * math.sin(2 * math.pi * x / 60.0 - phase * 0.8)
        )
        curr_y = baseline_y + y_offset
        wave_pts.append((x, curr_y))

    # Fill area under curve for glow effect
    glow_poly = [(wave_pts[0][0], 215)] + wave_pts + [(wave_pts[-1][0], 215)]
    draw.polygon(glow_poly, fill=(56, 189, 248, 25))

    # Draw waveform line with gradient segments
    for i in range(len(wave_pts) - 1):
        x_frac = wave_pts[i][0] / float(WIDTH)
        # Interpolate color: Cyan (6, 182, 212) -> Blue (59, 130, 246) -> Purple (168, 85, 247)
        if x_frac < 0.5:
            ratio = x_frac / 0.5
            r = int(6 * (1 - ratio) + 59 * ratio)
            g = int(182 * (1 - ratio) + 130 * ratio)
            b = int(212 * (1 - ratio) + 246 * ratio)
        else:
            ratio = (x_frac - 0.5) / 0.5
            r = int(59 * (1 - ratio) + 168 * ratio)
            g = int(130 * (1 - ratio) + 85 * ratio)
            b = int(246 * (1 - ratio) + 247 * ratio)
        draw.line([wave_pts[i], wave_pts[i+1]], fill=(r, g, b, 230), width=3)

    # 5. Glowing Pulsing Surveillance Nodes
    node_x_pos = [140, 280, 420, 550]
    node_colors = [
        (6, 182, 212),   # Cyan
        (59, 130, 246),  # Blue
        (99, 102, 241),  # Indigo
        (168, 85, 247),  # Purple
    ]
    for idx, nx in enumerate(node_x_pos):
        ny_offset = (
            18.0 * math.sin(2 * math.pi * nx / 240.0 - phase)
            + 9.0 * math.sin(2 * math.pi * nx / 110.0 + phase * 1.5)
            + 5.0 * math.sin(2 * math.pi * nx / 60.0 - phase * 0.8)
        )
        ny = baseline_y + ny_offset
        pulse = 0.5 + 0.5 * math.sin(phase * 2 + idx * 1.2)
        r_glow = 8 + int(pulse * 6)
        c = node_colors[idx]
        
        # Outer glow
        draw.ellipse([(nx - r_glow, ny - r_glow), (nx + r_glow, ny + r_glow)], fill=(c[0], c[1], c[2], 55))
        # Inner core
        draw.ellipse([(nx - 4, ny - 4), (nx + 4, ny + 4)], fill=(255, 255, 255, 240), outline=(c[0], c[1], c[2], 255), width=2)

    # 6. Feature Tags (y=226 to 254; well within safe area y <= 270)
    tags = [
        "Outbreak Tracking",
        "DHIS2 & SORMAS",
        "Epi & GIS Analytics",
        "Global Platforms"
    ]
    cur_x = 40
    tag_y = 228
    tag_h = 24
    for tag_text in tags:
        # compute tag width based on text
        tw = int(len(tag_text) * 7.2) + 20
        draw.rounded_rectangle(
            [(cur_x, tag_y), (cur_x + tw, tag_y + tag_h)],
            radius=6,
            fill=(30, 41, 59, 210),
            outline=(51, 65, 85, 200),
            width=1
        )
        draw.text((cur_x + 10, tag_y + 5), tag_text, font=font_tag, fill=(203, 213, 225, 240))
        cur_x += tw + 10

    # Composite overlay onto frame
    frame = Image.alpha_composite(frame, overlay)
    return frame.convert("RGB")

def main():
    print(f"Generating Social Preview GIF: {WIDTH}x{HEIGHT}px with {TOP_PADDING}px top/bottom padding...")
    fonts = get_fonts()
    base_bg = create_base_background()

    frames = []
    for f in range(TOTAL_FRAMES):
        rgb_frame = render_frame(f, base_bg, fonts)
        # Quantize to adaptive 128 colors for optimal size and smoothness
        paletted = rgb_frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(paletted)

    # Determine paths
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    out_dir = os.path.join(repo_root, "assets")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "social_preview.gif")

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True
    )

    size_bytes = os.path.getsize(out_path)
    size_kb = size_bytes / 1024.0
    print(f"Saved: {out_path}")
    print(f"Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"File size: {size_kb:.2f} KB ({size_bytes} bytes)")
    
    assert size_bytes < 1024 * 1024, f"File size exceeds 1MB: {size_bytes} bytes"
    print("SUCCESS: GIF strictly meets 640x320px and < 1MB requirements!")

if __name__ == "__main__":
    main()
