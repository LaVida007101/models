from facebook_scraper import get_posts, _scraper
import random
import json
import time

post_list = [] # Hold all posts extracted from the pages
pages = 1 # How many pages of post to request per facebook page


 # Generate a random delay between min_delay and max_delay seconds
def pause_scraping(min_delay=55, max_delay=73):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def return_post_list(latest_id=None):
    scrape_posts(latest_id)
    return post_list


# Get posts from FEU Tech ACM Facebook Page
def scrape_posts(latest_id):
    with open('./mbasicHeadersACM.json', 'r', encoding='utf-8') as file:
        _scraper.mbasic_headers = json.load(file)
    for post in get_posts('feutechACM', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechACM?v=timeline", pages=pages,
                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
                                    "allow_extra_requests": False,
                                    "comments": False,
                                    "reactors": False,
                                    "image_hop_timeout": 4,
                                    "HQ_images_max_count": 1}):
                                    
        new_dictionary = {
            'time': post.get('time', ''),
            'post_id': post.get('post_id', ''),
            'post_url': post.get('post_url', ''),
            'full_text': post.get('full_text', ''),
            'image_lowquality': post.get('image_lowquality', '')
        }
        if new_dictionary["post_id"] != latest_id:
            post_list.append(new_dictionary)
        else:
            break


    # pause_scraping()


    # # Get posts from FEU Tech AITS Facebook Page
    # with open('./mbasicHeadersAITS.json', 'r', encoding='utf-8') as file:
    #     _scraper.mbasic_headers = json.load(file)
    # for post in get_posts('feutechAITS', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechAITS?v=timeline", pages=pages,
    #                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
    #                                 "comments": False,
    #                                 "image_hop_timeout": 2,
    #                                 "HQ_images_max_count": 1}):
    #     new_dictionary = {
    #         'time': post.get('time', ''),
    #         'post_id': post.get('post_id', ''),
    #         'post_url': post.get('post_url', ''),
    #         'full_text': post.get('full_text', ''),
    #         'image_lowquality': post.get('image_lowquality', '')
    #     }
    #     post_list.append(new_dictionary)


    # pause_scraping()


    # # Get posts from FEU Tech Artist Connection Facebook Page
    # with open('./mbasicHeadersARTISTCONNECTION.json', 'r', encoding='utf-8') as file:
    #     _scraper.mbasic_headers = json.load(file)
    # for post in get_posts('feutechAC', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechAC?v=timeline", pages=pages,
    #                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
    #                                 "comments": False,
    #                                 "image_hop_timeout": 2,
    #                                 "HQ_images_max_count": 1}):
    #     new_dictionary = {
    #         'time': post.get('time', ''),
    #         'post_id': post.get('post_id', ''),
    #         'post_url': post.get('post_url', ''),
    #         'full_text': post.get('full_text', ''),
    #         'image_lowquality': post.get('image_lowquality', '')
    #     }
    #     post_list.append(new_dictionary)


    # pause_scraping()


    # # Get posts from FEU Tech SCC Facebook Page
    # with open('./mbasicHeadersFITITAMARAW.json', 'r', encoding='utf-8') as file:
    #     _scraper.mbasic_headers = json.load(file)
    # for post in get_posts('iTamarawsEsportsClub', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/iTamarawsEsportsClub?v=timeline", pages=pages,
    #                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
    #                                 "comments": False,
    #                                 "image_hop_timeout": 2,
    #                                 "HQ_images_max_count": 1}):
    #     new_dictionary = {
    #         'time': post.get('time', ''),
    #         'post_id': post.get('post_id', ''),
    #         'post_url': post.get('post_url', ''),
    #         'full_text': post.get('full_text', ''),
    #         'image_lowquality': post.get('image_lowquality', '')
    #     }
    #     post_list.append(new_dictionary)


    # pause_scraping()


    # # Get posts from FEU Tech SCC Facebook Page
    # with open('./mbasicHeadersMECS.json', 'r', encoding='utf-8') as file:
    #     _scraper.mbasic_headers = json.load(file)
    # for post in get_posts('FEUTechMEChS', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/FEUTechMEChS?v=timeline", pages=pages,
    #                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
    #                                 "comments": False,
    #                                 "image_hop_timeout": 2,
    #                                 "HQ_images_max_count": 1}):
    #     new_dictionary = {
    #         'time': post.get('time', ''),
    #         'post_id': post.get('post_id', ''),
    #         'post_url': post.get('post_url', ''),
    #         'full_text': post.get('full_text', ''),
    #         'image_lowquality': post.get('image_lowquality', '')
    #     }
    #     post_list.append(new_dictionary)


    # pause_scraping()


    # # Get posts from FEU Tech SCC Facebook Page
    # with open('./mbasicHeadersSCC.json', 'r', encoding='utf-8') as file:
    #     _scraper.mbasic_headers = json.load(file)
    # for post in get_posts('feutechscc', base_url="https://mbasic.facebook.com", start_url="https://mbasic.facebook.com/feutechscc?v=timeline", pages=pages,
    #                        options={"whitelist_methods": ["extract_post_id","extract_post_url", "extract_text", "extract_time", "extract_image_lq*"],
    #                                 "comments": False,
    #                                 "image_hop_timeout": 2,
    #                                 "HQ_images_max_count": 1}):
    #     new_dictionary = {
    #         'time': post.get('time', ''),
    #         'post_id': post.get('post_id', ''),
    #         'post_url': post.get('post_url', ''),
    #         'full_text': post.get('full_text', ''),
    #         'image_lowquality': post.get('image_lowquality', '')
    #     }
    #     post_list.append(new_dictionary)

for item in return_post_list():
    for detail in item:
        print(f"{detail} : {item[detail]}", '\n')
    print("\n\n\n\n")