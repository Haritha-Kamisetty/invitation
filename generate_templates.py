"""
Generate 80+ Professional Templates (20+ per category)
This script creates comprehensive template data for the invitation website
"""

import json

def generate_templates():
    templates = {
        "birthday": [],
        "wedding": [],
        "anniversary": [],
        "baby": []
    }
    
    # Birthday Templates (25 total)
    birthday_data = [
        ("Sunset Gradient", "Modern", "CELEBRATE WITH US\n{{host_name}}'s Birthday\n\n{{event_date}}\n{{event_time}}\n{{venue}}", "gradient_sunset"),
        ("Ocean Breeze", "Modern", "BIRTHDAY CELEBRATION\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_ocean"),
        ("Purple Haze", "Modern", "PARTY TIME!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_purple"),
        ("Mint Fresh", "Modern", "CELEBRATE\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_mint"),
        ("Coral Dream", "Modern", "JOIN US\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_coral"),
        ("Golden Hour", "Modern", "BIRTHDAY PARTY\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_gold"),
        ("Neon Lights", "Modern", "GLOW PARTY\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "neon"),
        ("Rose Quartz", "Modern", "CELEBRATE\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_rose"),
        ("Watercolor Blue", "Formal", "You're Invited\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_blue"),
        ("Watercolor Pink", "Formal", "JOIN US\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_pink"),
        ("Garden Watercolor", "Formal", "BIRTHDAY\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_green"),
        ("Lavender Watercolor", "Formal", "Please Join Us\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_purple"),
        ("Peach Watercolor", "Formal", "CELEBRATE\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_peach"),
        ("Rainbow Watercolor", "Playful", "PARTY!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_multi"),
        ("Geometric Gold", "Formal", "CELEBRATING\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "geometric_gold"),
        ("Silver Geometry", "Formal", "BIRTHDAY\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "geometric_silver"),
        ("Rose Gold Geometry", "Formal", "CELEBRATE\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "geometric_rose"),
        ("Navy Geometric", "Formal", "JOIN US\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "geometric_navy"),
        ("Teal Geometry", "Modern", "BIRTHDAY BASH\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "geometric_teal"),
        ("Art Deco", "Formal", "CELEBRATION\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "art_deco"),
        ("Confetti Party", "Playful", "PARTY TIME!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "confetti"),
        ("Tropical Paradise", "Playful", "ALOHA!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "tropical"),
        ("Balloon Party", "Playful", "CELEBRATE!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "balloon"),
        ("Retro Vibes", "Playful", "GROOVY BIRTHDAY\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "retro"),
        ("Disco Night", "Playful", "DISCO BASH\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "disco"),
    ]
    
    for i, (title, style, text, frame_type) in enumerate(birthday_data):
        templates["birthday"].append({
            "id": f"bday_{frame_type}",
            "title": title,
            "style": style,
            "text": text,
            "image": "",
            "frame": get_frame(frame_type)
        })
    
    # Wedding Templates (25 total)
    wedding_data = [
        ("Rose Gold Romance", "Formal", "Together with their families\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_rosegold"),
        ("Eucalyptus Garden", "Formal", "{{host_name}} & {{partner_name}}\nAre getting married!\n\n{{event_date}}\n{{venue}}", "watercolor_eucalyptus"),
        ("Navy Elegance", "Formal", "THE HONOR OF YOUR PRESENCE\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_navy"),
        ("Blush Minimalist", "Minimal", "{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "minimal_blush"),
        ("Bohemian Dreams", "Playful", "Join us\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "bohemian"),
        ("Lavender Fields", "Formal", "Wedding Celebration\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_lavender"),
        ("Sage Green", "Formal", "Together Forever\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_sage"),
        ("Dusty Rose", "Formal", "Getting Married\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_dustyrose"),
        ("Champagne Gold", "Formal", "Wedding Day\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_champagne"),
        ("Burgundy Elegance", "Formal", "Join Us\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_burgundy"),
        ("Ivory Classic", "Formal", "Wedding Invitation\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "classic_ivory"),
        ("Terracotta Sunset", "Modern", "Celebrate With Us\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_terracotta"),
        ("Midnight Blue", "Formal", "Wedding Ceremony\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_midnight"),
        ("Peach Blossom", "Formal", "We're Getting Married\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_peach"),
        ("Emerald Green", "Formal", "Join Our Celebration\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_emerald"),
        ("Copper Glow", "Modern", "Wedding Party\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_copper"),
        ("Lilac Dream", "Formal", "Together\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_lilac"),
        ("Coral Reef", "Modern", "Wedding Celebration\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_coralreef"),
        ("Slate Gray", "Minimal", "{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "minimal_slate"),
        ("Cream Lace", "Formal", "Wedding Invitation\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "lace_cream"),
        ("Garden Party", "Playful", "Celebrate!\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "garden"),
        ("Rustic Charm", "Playful", "Join Us\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "rustic"),
        ("Modern Marble", "Modern", "Wedding Day\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "marble"),
        ("Sunset Beach", "Playful", "Beach Wedding\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "beach_sunset"),
        ("Starry Night", "Formal", "Under The Stars\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "starry"),
    ]
    
    for i, (title, style, text, frame_type) in enumerate(wedding_data):
        templates["wedding"].append({
            "id": f"wed_{frame_type}",
            "title": title,
            "style": style,
            "text": text,
            "image": "",
            "frame": get_frame(frame_type)
        })
    
    # Anniversary Templates (20 total)
    anniversary_data = [
        ("Champagne Celebration", "Formal", "Celebrating Years of Love\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_champagne"),
        ("Ruby Romance", "Formal", "40 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_ruby"),
        ("Silver Shimmer", "Formal", "25 YEARS\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_silver"),
        ("Vintage Love", "Formal", "Love Story\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "vintage"),
        ("Sunset Together", "Modern", "YEARS OF LOVE\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_sunset"),
        ("Golden Jubilee", "Formal", "50 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_gold"),
        ("Pearl Anniversary", "Formal", "30 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "pearl"),
        ("Diamond Celebration", "Formal", "60 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "diamond"),
        ("Emerald Years", "Formal", "55 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_emerald"),
        ("Sapphire Love", "Formal", "45 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_sapphire"),
        ("Coral Anniversary", "Modern", "35 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_coral"),
        ("Crystal Clear", "Formal", "15 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "crystal"),
        ("Bronze Beauty", "Modern", "8 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_bronze"),
        ("Copper Glow", "Modern", "7 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_copper"),
        ("Iron Strong", "Modern", "6 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "gradient_iron"),
        ("Linen Love", "Formal", "4 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "linen"),
        ("Leather Legacy", "Modern", "3 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "leather"),
        ("Cotton Comfort", "Formal", "2 Years\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "cotton"),
        ("Paper Anniversary", "Minimal", "1 Year\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "paper"),
        ("Timeless Love", "Formal", "Anniversary\n{{host_name}} & {{partner_name}}\n\n{{event_date}}\n{{venue}}", "timeless"),
    ]
    
    for i, (title, style, text, frame_type) in enumerate(anniversary_data):
        templates["anniversary"].append({
            "id": f"ann_{frame_type}",
            "title": title,
            "style": style,
            "text": text,
            "image": "",
            "frame": get_frame(frame_type)
        })
    
    # Baby Shower Templates (20 total)
    baby_data = [
        ("Cloud Nine", "Playful", "A Little One!\nBaby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "clouds"),
        ("Pastel Rainbow", "Playful", "OH BABY!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "rainbow_pastel"),
        ("Woodland Wonder", "Formal", "Welcome Little One\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "woodland"),
        ("Twinkle Star", "Playful", "Twinkle Twinkle\nBaby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "stars"),
        ("Sweet Honey", "Formal", "Sweet as can bee!\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "honey"),
        ("Ocean Baby", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_ocean"),
        ("Pink Blush", "Formal", "Baby Girl Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_pink"),
        ("Blue Sky", "Formal", "Baby Boy Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_blue"),
        ("Mint Green", "Formal", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_mint"),
        ("Lavender Baby", "Formal", "Welcome Baby\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_lavender"),
        ("Sunshine Baby", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "gradient_yellow"),
        ("Peach Baby", "Formal", "Baby Celebration\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "watercolor_peach"),
        ("Safari Adventure", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "safari"),
        ("Elephant Love", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "elephant"),
        ("Butterfly Garden", "Formal", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "butterfly"),
        ("Moon & Stars", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "moon_stars"),
        ("Floral Baby", "Formal", "Welcome Baby\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "floral_baby"),
        ("Teddy Bear", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "teddy"),
        ("Rubber Ducky", "Playful", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "ducky"),
        ("Baby Feet", "Minimal", "Baby Shower\n{{host_name}}\n\n{{event_date}}\n{{venue}}", "minimal_feet"),
    ]
    
    for i, (title, style, text, frame_type) in enumerate(baby_data):
        templates["baby"].append({
            "id": f"baby_{frame_type}",
            "title": title,
            "style": style,
            "text": text,
            "image": "",
            "frame": get_frame(frame_type)
        })
    
    return templates

def get_frame(frame_type):
    """Generate SVG frame based on type"""
    frames = {
        # Gradients
        "gradient_sunset": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23ff6b6b'/%3E%3Cstop offset='50%25' style='stop-color:%23feca57'/%3E%3Cstop offset='100%25' style='stop-color:%23ee5a6f'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_ocean": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%2300d2ff'/%3E%3Cstop offset='100%25' style='stop-color:%233a7bd5'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_purple": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%238e44ad'/%3E%3Cstop offset='100%25' style='stop-color:%23c0392b'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_mint": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%2355efc4'/%3E%3Cstop offset='100%25' style='stop-color:%2300b894'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_coral": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23ff7675'/%3E%3Cstop offset='100%25' style='stop-color:%23fd79a8'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_gold": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23f39c12'/%3E%3Cstop offset='100%25' style='stop-color:%23e74c3c'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        "gradient_rose": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23f8b4d9'/%3E%3Cstop offset='100%25' style='stop-color:%23ffd1dc'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3C/svg%3E",
        # Watercolors
        "watercolor_blue": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='%23f0f8ff'/%3E%3Ccircle cx='20%25' cy='20%25' r='150' fill='%2387ceeb' opacity='0.3'/%3E%3Ccircle cx='80%25' cy='80%25' r='200' fill='%234682b4' opacity='0.2'/%3E%3C/svg%3E",
        "watercolor_pink": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='%23fff5f7'/%3E%3Ccircle cx='30%25' cy='30%25' r='120' fill='%23ffb6c1' opacity='0.25'/%3E%3Ccircle cx='70%25' cy='70%25' r='180' fill='%23ff69b4' opacity='0.2'/%3E%3C/svg%3E",
        # Add more frame types...
        "neon": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='%23000'/%3E%3Crect x='10' y='10' width='calc(100%25-20px)' height='calc(100%25-20px)' fill='none' stroke='%2300ff00' stroke-width='3' opacity='0.8'/%3E%3C/svg%3E",
        "confetti": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='%23fff9e6'/%3E%3Ccircle cx='10%25' cy='15%25' r='8' fill='%23ff6b9d'/%3E%3Ccircle cx='90%25' cy='20%25' r='12' fill='%23c44569'/%3E%3Ccircle cx='15%25' cy='80%25' r='10' fill='%23ffa502'/%3E%3C/svg%3E",
        "tropical": "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%2300d2ff'/%3E%3Cstop offset='100%25' style='stop-color:%233a7bd5'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)'/%3E%3Ccircle cx='15%25' cy='85%25' r='60' fill='%2300b894' opacity='0.4'/%3E%3C/svg%3E",
    }
    
    # Return frame or default white background
    return frames.get(frame_type, "data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='100%25' height='100%25' fill='%23ffffff'/%3E%3C/svg%3E")

if __name__ == "__main__":
    templates = generate_templates()
    
    # Print summary
    print(f"Generated {sum(len(v) for v in templates.values())} templates:")
    for category, items in templates.items():
        print(f"  {category}: {len(items)} templates")
    
    # Save to JSON for reference
    with open("templates_output.json", "w") as f:
        json.dump(templates, f, indent=2)
    
    print("\nTemplates saved to templates_output.json")
