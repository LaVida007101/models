import re

def remove_links_and_hashtags(text):
    # Regular expression to match URLs
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'bit\.ly/[a-zA-Z0-9]+'
    )
    
    # Regular expression to match hashtags
    hashtag_pattern = re.compile(r'#\S+')
    
    # Replace URLs and hashtags with an empty string
    text = re.sub(url_pattern, '', text)
    text = re.sub(hashtag_pattern, '', text)
    
    return text

