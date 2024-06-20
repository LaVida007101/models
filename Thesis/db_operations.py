from dateutil import parser
from datetime import datetime, timedelta
from firebase_admin import db
from firebase_admin import credentials, storage

import os
import re
import requests
import firebase_admin

def initialize_db_connection():
    dirname = os.path.dirname(__file__)
    file_name = os.path.join(dirname, 'db_key/giftver3-firebase-adminsdk-nk1a5-5d405a7743.json')
    cred = credentials.Certificate(file_name)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://giftver3-default-rtdb.firebaseio.com/',
        'storageBucket': 'giftver3.appspot.com'
    })

# def get_day_of_week(date_str):
#     try:
#         # Parse the date string into a datetime object
#         date_obj = parser.parse(date_str)
        
#         # Get the day of the week as a string (e.g., "Monday")
#         day_of_week = date_obj.strftime('%A')
        
#         return day_of_week
#     except ValueError:
#         return "Invalid date format"

def get_day_of_week(date_str):
    try:
        # Regular expressions to identify date patterns
        range_regex = r"(\d{1,2})\s*(-|–|to)\s*(\d{1,2})"
        single_date_regex = r"(\d{1,2})(?:th|st|nd|rd)?\s+of\s+(\w+)\s*(\d{4})?"

        # Remove time information since it's irrelevant
        date_str = re.sub(r'\d{1,2}:\d{2}\s*(AM|PM)?\s*-\s*\d{1,2}:\d{2}\s*(AM|PM)?', '', date_str)
        date_str = re.sub(r'\d{1,2}:\d{2}\s*(AM|PM)?', '', date_str)
        date_str = re.sub(r'from\s*\d{1,2}:\d{2}\s*(AM|PM)?\s*to\s*\d{1,2}:\d{2}\s*(AM|PM)?', '', date_str, flags=re.IGNORECASE)
        
        # Remove additional "from" and "to" keywords
        date_str = re.sub(r'\bfrom\b', '', date_str, flags=re.IGNORECASE)
        date_str = re.sub(r'\bto\b', '', date_str, flags=re.IGNORECASE)

        # Parse single dates like "24th of February" and "24th of February 2024"
        match = re.search(single_date_regex, date_str, re.IGNORECASE)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3) if match.group(3) else str(datetime.now().year)
            single_date = f"{month} {day}, {year}"
            date_obj = parser.parse(single_date)
            return [date_obj.strftime('%A')]
        
        # Parse date ranges
        match = re.search(range_regex, date_str)
        if match:
            start_day = int(match.group(1))
            end_day = int(match.group(3))
            month_year = re.sub(range_regex, '', date_str).strip().replace('from', '').replace('-', '').replace('–', '').replace('to', '')
            month_year = re.sub(r'\s+', ' ', month_year).strip()
            
            start_date = parser.parse(f"{month_year} {start_day}")
            end_date = parser.parse(f"{month_year} {end_day}")
            
            days_of_week = []
            current_date = start_date
            while current_date <= end_date:
                days_of_week.append(current_date.strftime('%A'))
                current_date += timedelta(days=1)
            
            return days_of_week
        
        # If no specific format is matched, try to parse normally
        date_obj = parser.parse(date_str)
        return [date_obj.strftime('%A')]
    
    except Exception as e:
        return ["Invalid date format"]
    

def write_events_to_db(event_details):

    # Reference to the database
    root_ref = db.reference('upcoming_events')

    for event in event_details:
        new_event_ref = root_ref.push()
        new_event_ref.update(event)


def maintain_events_in_db():

    # Reference to the database
    events_ref = db.reference('upcoming_events')

    events = events_ref.get()

    for event_id, event_details in events:
        if 'date' in event_details:
            date_differrence = calculate_date_difference(event_details['date'])
            
        if date_differrence < 0:
            events_ref.child(event_id).delete()
        
def get_user_data():
    categories = [
    "Celebrations",
    "Software Engineering",
    "Information Technology",
    "Data Science",
    "Computer Science",
    "Conference",
    "Reviews and Study Sessions",
    "Career Developments",
    "Online Events",
    "Competitions",
    "Guest Speakers",
    "Gaming",
    "Creativity and Artistry",
    "Performing Arts and Talents",
    "Computer Engineering",
    "Spiritual",
]


    # Reference to the database
    events_ref = db.reference('upcoming_events')
    users_ref = db.reference('users')

    users = users_ref.get()
    events = events_ref.get()

    results = []

    def day_of_week_to_index(day_input):
      days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
      days_list = []
      for day in day_input:
          days_list.append(days.index(day.lower()))
      return days_list

    # Iterate through each user
    for user_id, user_details in users.items():
        user_session_records = user_details.get('session_records', {})
        session_dict = {}
        
        saved_events = []
        for id, detail in user_details.get('saved_events', {}).items():
            if isinstance(detail, dict):
                event_id = detail.get("details")
            if isinstance(id, dict):
                event_id = event_id.get("id")
            saved_events.append(event_id)

        saved_category_in_saved_events_count = {}
        days_of_week_in_saved_events = [0] * 7

        for id, details in events.items():
             event_id = None
             event_details = None
             event_id = details.get("id")
             event_details = details.get("details")

            #  import sys
            #  sys.exit()
            #  for key, value in event.items():
            #     if key == "details":
            #         event_details = value
            #     elif key == "id":
            #         event_id = value
             if event_id in saved_events:
                for category in event_details['category']:
                    if category in saved_category_in_saved_events_count:
                        saved_category_in_saved_events_count[category] += 1
                    else:
                        saved_category_in_saved_events_count[category] = 1

                date_day = get_day_of_week(event_details['date'])
                index = day_of_week_to_index(date_day)
                for day in index:
                    days_of_week_in_saved_events[day] += 1


        # Iterate through each category in session records
        for category, category_details in user_session_records.items():
            if isinstance(category_details, dict):
                # Extract values from the dictionary
                values = list(category_details.values())
            elif isinstance(category_details, list):
                # If already a list, use it directly
                values = category_details
            else:
                # Skip if the category details are not in expected format
                continue
            
            if category in saved_category_in_saved_events_count:
                values.append(saved_category_in_saved_events_count[category])
            else:
                values.append(0)

            session_dict[category] = values

        for category in categories:
            if category not in session_dict:
                session_dict[category] = [0,0,0]
        session_dict['days'] = days_of_week_in_saved_events
        if session_dict:
            results.append({user_id: session_dict})

    return results

def get_event_data():
    events_ref = db.reference('upcoming_events')
    events = events_ref.get()
    results = {}

    def day_of_week_to_index(day_input):
      days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
      days_list = []
      for day in day_input:
          days_list.append(days.index(day.lower()))
      return days_list
    
    
    for id, detail in events.items():
        event_id = detail.get("id")
        event_details = detail.get("details")
        
        date_day = get_day_of_week(event_details['date'])
        day_index = day_of_week_to_index(date_day)
        days_index = [0] * 7
        for day in day_index:
            days_index[day] += 1
        results[event_id] =  [event for event in event_details['category']] + [days_index]
        

    return results

def add_recommended(user_id, event):
    events_ref = db.reference('upcoming_events')
    users_ref = db.reference('users')

    users = users_ref.get()
    events = events_ref.get()

    for id, detail in events.items():
        event_details = detail.get("details")
        if event_details["id"] == event:
            recommended_events_ref = users_ref.child(user_id).child('recommended_events')
            if 'recommended_events' in users[user_id]:
                new_event_ref = recommended_events_ref.push()
                new_event_ref.update(detail)

            else:
                new_event_ref = recommended_events_ref.push()
                new_event_ref.set(detail)
                # users_ref.child(user_id).child('recommended_events').set([])
            # new_event_ref = root_ref.push()
            # new_event_ref.update(event)


def calculate_date_difference(date1: str, date2: str = datetime.now().strftime('%m-%d-%Y')) -> int:
    # List of possible date formats
    date_formats = ["%m-%d-%Y", "%B %d, %Y"]
    
    def parse_date(date_str):
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        raise ValueError("Date format not recognized")
    
    # Parse the input dates
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    
    difference = (d1 - d2).days
    
    return difference

def download_upload_get_url(image_url, name):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content

        bucket = storage.bucket()
        blob = bucket.blob(f"event_images/{name}.jpg")  
        blob.upload_from_string(image_data, content_type='image/jpeg')

        expiration_time = datetime.now() + timedelta(days=365 * 100)  
        download_url = blob.generate_signed_url(expiration=expiration_time, method='GET')

        return download_url
    else:
        return '''Image link has returned an error'''

# initialize_db_connection()
# # users = get_user_data()
# users = get_user_data()
# for user in users:
#     for id, category in user.items():
#         print(id)
#     print(user, "\n\n")
    
# for user, details in users:
#     print(user, ': ', details, '\n')
# events = get_event_data()
# for event in events:
#     print(event, '\n')

# dirname = os.path.dirname(__file__)
# file_name = os.path.join(dirname, 'db_key/giftver3-firebase-adminsdk-nk1a5-5d405a7743.json')
# cred = credentials.Certificate(file_name)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://giftver3-default-rtdb.firebaseio.com/',
#     'storageBucket': 'giftver3.appspot.com'
# })

# root_ref = db.reference('/')

# root_ref.update({
#   "upcoming_events": [
#     {
#       "details":{
#       "category": [
#         "Conference",
#         "Computer Engineering"
#       ],
#       "date": "June 19, 2024",
#       "description": "on June 19, 2024, we will explore the future of coding with Barangay 842, Pandacan, Manila’s best and brightest!",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F2.png?alt=media&token=0497bb71-dbef-4be9-bd15-4366dcba3851",
#       "link": "https://www.facebook.com/photo/?fbid=877686364401204&set=a.470381998464978",
#       "location": "FEU TECH F1012",
#       "name": "Craft the Code: Discover the Future of Coding"
#       },
#       "id": "2gdhyt789dagd"
#     },
#     {
#       "details":{
#       "category": [
#         "Celebration"
#       ],
#       "date": "June 28",
#       "description": "GET READY TO BE TRANSPORTED TO THE FARTHEST REACHES OF THE GALAXY! Featuring stellar performances, cosmic vibes, and a night full of music and fun",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F5.png?alt=media&token=18e6c0eb-1568-4a81-a804-19e825dcbb88",
#       "link": "https://www.facebook.com/photo/?fbid=915068797326613&set=a.583605170472979",
#       "location": "𝗙𝗘𝗨 𝗠𝗔𝗡𝗜𝗟𝗔 𝗚𝗥𝗔𝗡𝗗𝗦𝗧𝗔𝗡𝗗",
#       "name": "𝗜𝗧𝗔𝗠 𝗡𝗜𝗚𝗛𝗧 𝟮𝟬𝟮𝟰: 𝗧𝗛𝗥𝗢𝗨𝗚𝗛 𝗧𝗛𝗘 𝗖𝗢𝗦𝗠𝗢𝗦"
#       },
#       "id": "hrye67gs5423"
#     },
#     {
#       "details": {
#       "category": [
#         "Guest Speakers",
#         "Conference"
#       ],
#       "date": "June 22, 2024",
#       "description": "ACM 17YSTOPIA sets off to venture onwards, to The Future of Tech  . prepare for informative talks as we tackle Emerging Technologies and Their Impact . Join the kick-off of FEU Tech ACM's 17 year anniversary, and register now, for a free pass to the conference .",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F448207627_799255432311755_178748510803207155_n.jpg?alt=media&token=d539dedc-62da-4c00-af30-517b92ca53e9",
#       "link": "https://www.facebook.com/photo/?fbid=799255228978442&set=a.519143656989602",
#       "location": "TBA",
#       "name": "ACM 17YSTOPIA"
#        },
#        "id": "jhbtybqrk23"
#     }
#   ],
#   "banner_events": [
#     {
#       "details":{
#       "category": [
#         "Conference",
#         "Computer Engineering"
#       ],
#       "date": "June 19, 2024",
#       "description": "on June 19, 2024, we will explore the future of coding with Barangay 842, Pandacan, Manila’s best and brightest!",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F2.png?alt=media&token=0497bb71-dbef-4be9-bd15-4366dcba3851",
#       "link": "https://www.facebook.com/photo/?fbid=877686364401204&set=a.470381998464978",
#       "location": "FEU TECH F1012",
#       "name": "Craft the Code: Discover the Future of Coding"
#       },
#       "id": "2gdhyt789dagd"
#     },
#     {
#       "details":{
#       "category": [
#         "Celebration"
#       ],
#       "date": "June 28",
#       "description": "GET READY TO BE TRANSPORTED TO THE FARTHEST REACHES OF THE GALAXY! Featuring stellar performances, cosmic vibes, and a night full of music and fun",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F5.png?alt=media&token=18e6c0eb-1568-4a81-a804-19e825dcbb88",
#       "link": "https://www.facebook.com/photo/?fbid=915068797326613&set=a.583605170472979",
#       "location": "𝗙𝗘𝗨 𝗠𝗔𝗡𝗜𝗟𝗔 𝗚𝗥𝗔𝗡𝗗𝗦𝗧𝗔𝗡𝗗",
#       "name": "𝗜𝗧𝗔𝗠 𝗡𝗜𝗚𝗛𝗧 𝟮𝟬𝟮𝟰: 𝗧𝗛𝗥𝗢𝗨𝗚𝗛 𝗧𝗛𝗘 𝗖𝗢𝗦𝗠𝗢𝗦"
#       },
#       "id": "hrye67gs5423"
#     },
#     {
#       "details": {
#       "category": [
#         "Guest Speakers",
#         "Conference"
#       ],
#       "date": "June 22, 2024",
#       "description": "ACM 17YSTOPIA sets off to venture onwards, to The Future of Tech  . prepare for informative talks as we tackle Emerging Technologies and Their Impact . Join the kick-off of FEU Tech ACM's 17 year anniversary, and register now, for a free pass to the conference .",
#       "image_link": "https://firebasestorage.googleapis.com/v0/b/giftver3.appspot.com/o/event_images%2F448207627_799255432311755_178748510803207155_n.jpg?alt=media&token=d539dedc-62da-4c00-af30-517b92ca53e9",
#       "link": "https://www.facebook.com/photo/?fbid=799255228978442&set=a.519143656989602",
#       "location": "TBA",
#       "name": "ACM 17YSTOPIA"
#        },
#        "id": "jhbtybqrk23"
#     }
#   ]
# })