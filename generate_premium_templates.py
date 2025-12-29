"""
Generate BOLD & VIBRANT Invitation Templates
Focus: Deep saturated colors, high contrast, and rich textures.
Constraint: ONLY ONE plain white template total.
"""

import json
import urllib.parse

def create_noise_filter_def():
    return '''
    <filter id="noise" x="0%" y="0%" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
        <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.1 0"/>
    </filter>
    <filter id="gold-foil">
        <feTurbulence type="fractalNoise" baseFrequency="0.2" numOctaves="3" result="noise"/>
        <feDiffuseLighting in="noise" lighting-color="#ffd700" surfaceScale="3">
            <feDistantLight azimuth="45" elevation="60"/>
        </feDiffuseLighting>
        <feComposite operator="in" in2="SourceGraphic"/>
    </filter>
    <filter id="watercolor" x="-20%" y="-20%" width="140%" height="140%">
        <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="1"/>
        <feDisplacementMap in="SourceGraphic" scale="20" />
        <feGaussianBlur stdDeviation="5" />
    </filter>
    '''

def get_svg_frame(style, colors, texture=False, motif=None):
    """
    Generates a complex SVG background based on style parameters.
    """
    defs = create_noise_filter_def()
    
    # Common Patterns
    pattern_defs = '''
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    </pattern>
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
        <circle cx="2" cy="2" r="1.5" fill="rgba(255,255,255,0.2)"/>
    </pattern>
    <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#bf953f" />
        <stop offset="25%" stop-color="#fcf6ba" />
        <stop offset="50%" stop-color="#b38728" />
        <stop offset="75%" stop-color="#fbf5b7" />
        <stop offset="100%" stop-color="#aa771c" />
    </linearGradient>
    '''
    
    # Safe color accessor
    def get_col(idx, default="#000"):
        return colors[idx] if idx < len(colors) else (colors[0] if len(colors) > 0 else default)

    # Motif Paths
    motifs = {
        "leaves": '<path d="M0,0 C20,50 80,50 100,100" stroke="#4a6741" stroke-width="2" fill="none" opacity="0.3"/>',
        "floral_corner": f'''
            <g transform="translate(-20,-20) scale(1.5)">
                <circle cx="50" cy="50" r="30" fill="url(#grad1)" opacity="0.9"/>
                <circle cx="80" cy="40" r="20" fill="url(#grad1)" opacity="0.7"/>
                <path d="M50,50 Q80,20 100,50 T150,50" stroke="rgba(255,255,255,0.3)" stroke-width="3" fill="none"/>
            </g>
            <g transform="translate(calc(100% - 100px), calc(100% - 100px)) scale(1.5) rotate(180 50 50)">
                 <circle cx="50" cy="50" r="30" fill="url(#grad1)" opacity="0.9"/>
            </g>
        ''',
        "abstract_shapes": f'''
            <circle cx="10%" cy="10%" r="150" fill="{get_col(1)}" opacity="0.9"/>
            <circle cx="90%" cy="90%" r="200" fill="{get_col(1)}" opacity="0.8"/>
            <rect x="80%" y="10%" width="100" height="100" transform="rotate(45)" fill="rgba(255,255,255,0.15)"/>
        '''
    }

    content = ""
    
    # Background Base - BOLD COLORS
    if texture == "paper":
        content += f'<rect width="100%" height="100%" fill="{get_col(0)}"/>' # Dark base
        content += '<rect width="100%" height="100%" filter="url(#noise)" opacity="0.4"/>' # Visible texture
    elif texture == "noise":
        content += f'<rect width="100%" height="100%" fill="{get_col(0)}"/>'
        content += '<rect width="100%" height="100%" filter="url(#noise)" opacity="0.3"/>'
    elif style == "gradient":
        defs += f'''
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{get_col(0)}" />
            <stop offset="100%" stop-color="{get_col(1)}" />
        </linearGradient>
        '''
        content += '<rect width="100%" height="100%" fill="url(#grad1)"/>'
    else:
        content += f'<rect width="100%" height="100%" fill="{get_col(0)}"/>'

    # Add Motifs/Decorations - HIGH CONTRAST
    if motif == "floral":
        defs += f'''
        <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" stop-color="{get_col(1, '#ffeb3b')}" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="{get_col(1, '#ffeb3b')}" stop-opacity="0"/>
        </radialGradient>
        '''
        content += motifs["floral_corner"]
    
    elif motif == "watercolor":
        defs += f'''
        <radialGradient id="splash1" cx="30%" cy="30%" r="40%">
            <stop offset="0%" stop-color="{get_col(1, '#ff0055')}" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="{get_col(1, '#ff0055')}" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="splash2" cx="70%" cy="80%" r="50%">
            <stop offset="0%" stop-color="{get_col(2, get_col(1, '#00ccff'))}" stop-opacity="0.7"/>
            <stop offset="100%" stop-color="{get_col(1, '#00ccff')}" stop-opacity="0"/>
        </radialGradient>
        '''
        content += f'''
        <rect width="100%" height="100%" fill="{get_col(0)}"/>
        <circle cx="30%" cy="30%" r="200" fill="url(#splash1)" filter="url(#watercolor)"/>
        <circle cx="80%" cy="80%" r="250" fill="url(#splash2)" filter="url(#watercolor)"/>
        '''

    elif motif == "border_gold":
        content += '''
        <rect x="20" y="20" width="calc(100% - 40px)" height="calc(100% - 40px)" fill="none" stroke="url(#gold-grad)" stroke-width="6"/>
        <rect x="15" y="15" width="calc(100% - 30px)" height="calc(100% - 30px)" fill="none" stroke="url(#gold-grad)" stroke-width="2" opacity="0.7"/>
        '''

    elif motif == "pattern_geo":
         content += '<rect width="100%" height="100%" fill="url(#grid)"/>'

    elif motif == "dots":
         content += '<rect width="100%" height="100%" fill="url(#dots)"/>'

    elif motif == "abstract_shapes":
         content += motifs["abstract_shapes"]

    # Assemble Raw SVG
    raw_svg = f'<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><defs>{defs}{pattern_defs}</defs>{content}</svg>'
    
    # URL Encode
    encoded = urllib.parse.quote(raw_svg)
    return f'data:image/svg+xml,{encoded}'

def generate_templates():
    templates = {
        "birthday": [],
        "wedding": [],
        "anniversary": [],
        "baby": []
    }

    # --- Birthday (25 Designs) - BOLD & FUN ---
    # 1. The ONLY White Template
    templates["birthday"].append({
        "id": "bday_clean_white",
        "title": "Clean Minimalist",
        "style": "Minimal",
        "text": "BIRTHDAY\n{{host_name}}\n{{event_date}}",
        "image": "",
        "frame": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='white'/%3E%3C/svg%3E"
    })

    # Deep/Vibrant Colors - NO PASTELS
    bday_bold = [
        ("Midnight Blue", ["#0a192f", "#64ffda"], "noise", "abstract_shapes", "Modern"),
        ("Electric Purple", ["#4c1d95", "#c4b5fd"], "noise", "dots", "Party"),
        ("Neon Pink", ["#be185d", "#fbcfe8"], "gradient", "abstract_shapes", "Fun"),
        ("Deep Teal", ["#134e4a", "#2dd4bf"], "paper", "border_gold", "Elegant"),
        ("Sunset Orange", ["#c2410c", "#fdba74"], "gradient", "dots", "Warm"),
        ("Royal Gold", ["#78350f", "#fcd34d"], "noise", "border_gold", "Luxury"),
        ("Charcoal Minimal", ["#18181b", "#e4e4e7"], "paper", "abstract_shapes", "Modern"),
        ("Ruby Red", ["#991b1b", "#fecaca"], "gradient", "dots", "Bold"),
        ("Forest Green", ["#14532d", "#86efac"], "noise", "floral", "Nature"),
        ("Ocean Depth", ["#1e3a8a", "#60a5fa"], "gradient", "watercolor", "Cool"),
    ]
    for t, c, tex, m, s in bday_bold:
        templates["birthday"].append({"title": t, "style": s, "colors": c, "texture": tex if tex != "gradient" else None, "style_type": tex if tex == "gradient" else None, "motif": m})

    # Fillers with strong colors
    for i in range(14):
        hue = (i * 30) % 360
        color = f"hsl({hue}, 70%, 40%)" # Dark saturated background
        accent = f"hsl({hue}, 70%, 80%)"
        templates["birthday"].append({"title": f"Vibrant Party {i+1}", "style": "Fun", "colors": [color, accent], "motif": "dots"})


    # --- Wedding (25 Designs) - DARK LUXURY ---
    wed_designs = [
        ("Royal Navy Gold", ["#0a192f", "#ffd700"], "noise", "border_gold", "Luxury"),
        ("Emerald Velvet", ["#064e3b", "#d1fae5"], "paper", "floral", "Elegant"),
        ("Burgundy Wine", ["#450a0a", "#fecaca"], "paper", "border_gold", "Romantic"),
        ("Charcoal & Gold", ["#111827", "#fde68a"], "noise", "border_gold", "Modern"),
        ("Deep Plum", ["#4c1d95", "#ddd6fe"], "paper", "floral", "Majestic"),
        ("Black Tie", ["#000000", "#ffffff"], "noise", "border_gold", "Formal"),
        ("Midnight Star", ["#1e1b4b", "#e0e7ff"], "gradient", "dots", "Celestial"),
        ("Rich Chocolate", ["#3f2c22", "#f5d0b0"], "paper", "border_gold", "Vintage"),
        ("Sapphire Night", ["#172554", "#bfdbfe"], "noise", "watercolor", "Blue"),
        ("Crimson Love", ["#7f1d1d", "#fca5a5"], "paper", "floral", "Passion"),
    ]
    for t, c, tex, m, s in wed_designs:
        templates["wedding"].append({"title": t, "style": s, "colors": c, "texture": tex if tex != "gradient" else None, "style_type": tex if tex == "gradient" else None, "motif": m})
    
    for i in range(15):
        templates["wedding"].append({"title": f"Luxury Wedding {i+1}", "style": "Formal", "colors": ["#1a1a1a", "#d4af37"], "motif": "border_gold"})


    # --- Anniversary (20 Designs) - METALLIC & BOLD ---
    ann_designs = [
        ("Golden 50th", ["#000000", "#ffd700"], "gradient", "border_gold", "Luxury"),
        ("Silver 25th", ["#1f2937", "#e5e7eb"], "gradient", "border_gold", "Classic"),
        ("Ruby 40th", ["#881337", "#fb7185"], "noise", "watercolor", "Romantic"),
        ("Sapphire 45th", ["#1e3a8a", "#93c5fd"], "paper", "border_gold", "Blue"),
        ("Emerald 55th", ["#065f46", "#6ee7b7"], "paper", "floral", "Green"),
        ("Bronze 8th", ["#451a03", "#fdba74"], "noise", "dots", "Warm"),
        ("Pearl 30th", ["#374151", "#f9fafb"], "paper", "dots", "Elegant"),
        ("Diamond 60th", ["#0f172a", "#38bdf8"], "gradient", "abstract_shapes", "Modern"),
    ]
    for t, c, tex, m, s in ann_designs:
        templates["anniversary"].append({"title": t, "style": s, "colors": c, "texture": tex if tex != "gradient" else None, "style_type": tex if tex == "gradient" else None, "motif": m})
    
    while len(templates["anniversary"]) < 20:
        templates["anniversary"].append({"title": f"Anniversary Gala {len(templates['anniversary'])}", "style": "Elegant", "colors": ["#2c2c2c", "#fff"], "motif": "border_gold"})

    # --- Baby Shower (20 Designs) - BRIGHT & CHEERFUL ---
    baby_designs = [
        ("Vibrant Yellow", ["#fbbf24", "#fffbeb"], "gradient", "dots", "Bright"),
        ("Deep Sky Blue", ["#0284c7", "#bae6fd"], "paper", "abstract_shapes", "Boy"),
        ("Hot Pink Pop", ["#db2777", "#fbcfe8"], "noise", "watercolor", "Girl"),
        ("Lush Jungle", ["#15803d", "#86efac"], "paper", "leaves", "Safari"),
        ("Purple Play", ["#7c3aed", "#ddd6fe"], "gradient", "dots", "Fun"),
        ("Orange Zest", ["#ea580c", "#fed7aa"], "noise", "watercolor", "Energy"),
        ("Teal Toybox", ["#0d9488", "#99f6e4"], "paper", "grid", "Modern"),
        ("Navy Night", ["#172554", "#fde047"], "gradient", "stars", "Sleepy"),
    ]
    for t, c, tex, m, s in baby_designs:
        templates["baby"].append({"title": t, "style": s, "colors": c, "texture": tex if tex != "gradient" else None, "style_type": tex if tex == "gradient" else None, "motif": m})

    while len(templates["baby"]) < 20:
         templates["baby"].append({"title": f"Baby Shower Fun {len(templates['baby'])}", "style": "Cute", "colors": ["#0ea5e9", "#fff"], "motif": "dots"})


    # Convert abstract dicts to full template objects
    final_templates = {}
    
    for category, items in templates.items():
        final_templates[category] = []
        for i, item in enumerate(items):
            # If it's already a full template (like the white one)
            if "id" in item:
                final_templates[category].append(item)
                continue
                
            # Generate ID
            t_id = f"{category[:3]}_{i}_{item['title'].lower().replace(' ', '_')}"
            
            # Generate SVG
            svg = get_svg_frame(
                style=item.get("style_type", "flat"),
                colors=item.get("colors", ["#000"]),
                texture=item.get("texture", False),
                motif=item.get("motif", None)
            )
            
            # Standard Text
            default_text = f"JOIN US FOR A\n{item['title'].upper()}\n\n{{{{host_name}}}}\n\n{{{{event_date}}}} @ {{{{event_time}}}}\n{{{{venue}}}}"
            
            final_templates[category].append({
                "id": t_id,
                "title": item["title"],
                "style": item["style"],
                "text": default_text,
                "image": "",
                "frame": svg
            })

    return final_templates

if __name__ == "__main__":
    t = generate_templates()
    with open("templates_output.json", "w", encoding='utf-8') as f:
        json.dump(t, f, indent=4)
    print("Generated BOLD & VIBRANT Templates JSON")
