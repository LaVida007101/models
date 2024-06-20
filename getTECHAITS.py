from facebook_scraper import get_posts, _scraper
import json

with open('./mbasicHeadersAITS.json', 'r') as file:
    _scraper.mbasic_headers = json.load(file)

for post in get_posts('feutechAITS', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechAITS?v=timeline", pages=1,
                       options={"whitelist_methods": ["extract_post_url", "extract_text", "extract_time", "extract_image_lq*"]}):
    print(post)
    print("---------------------------------------------------------------------------------------------------------------------------------------------")
