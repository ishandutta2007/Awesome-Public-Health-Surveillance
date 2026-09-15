---
name: generate-social-preview-gif
description: >-
  Generates an animated Social Preview GIF (strictly 640x320px, <1MB in size, with 50px top and bottom padding)
  mirroring the visual branding, colors, and dynamic behavior of the repository's banner for GitHub social card previews.
---

# Generate Social Preview GIF

Use this skill when you need to generate or update an animated `social_preview.gif` image for repository social card previews.

## Specifications & Requirements

- **Output Path**: `assets/social_preview.gif`
- **Format**: Animated GIF (looping)
- **Dimensions**: Exactly `640x320` px
- **File Size**: Strictly `< 1 MB` (< 1,048,576 bytes)
- **Safe Area & Padding**: Strictly `50px` padding on both top and bottom (vertical content bounded between `y = 50` and `y = 270`) to prevent cropping on GitHub preview cards.
- **Visuals**: Matches repository banner color scheme (dark background `#0f172a` / `#1e1b4b`, grid overlay, glowing wave signal, glowing pulsing nodes, pill badge, title, subtitle, and feature tags).

## Directory Structure

```text
.agents/skills/generate-social-preview-gif/
├── SKILL.md
└── scripts/
    └── generate_gif.py
```

## How to Run

Execute the bundled Python script:

```bash
python .agents/skills/generate-social-preview-gif/scripts/generate_gif.py
```

The script will:
1. Render multi-frame animated sequences with moving wave signal and pulsing nodes using Pillow and NumPy.
2. Ensure vertical layout adheres strictly to safe boundaries (`y: 50` to `y: 270`).
3. Quantize frames with adaptive palettes to guarantee file size remains comfortably under 1MB (~545 KB).
4. Output directly to `assets/social_preview.gif`.
