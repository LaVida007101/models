from facebook_scraper import get_posts, _scraper
import json

with open('./mbasicHeadersSCC.json', 'r', encoding='utf-8') as file:
    _scraper.mbasic_headers = json.load(file)

for post in get_posts('feutechscc', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechscc?v=timeline", pages=1,
                       options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
                                "comments": False,
                                "image_hop_timeout": 2,
                                "HQ_images_max_count": 1}):
    for item in post:
        print(f"{item} : {post[item]}", "\n")
    print("\n\n\n")
    break
