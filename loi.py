import requests
import time

# Indra Logo
INDRA_LOGO = """
 █████  ███    ██ ██████   █████  ██████  
██   ██ ████   ██ ██   ██ ██   ██ ██   ██ 
███████ ██ ██  ██ ██   ██ ███████ ██████  
██   ██ ██  ██ ██ ██   ██ ██   ██ ██   ██ 
██   ██ ██   ████ ██████  ██   ██ ██   ██ 
"""
print(INDRA_LOGO)

# Load Cookies
def load_cookies():
    cookies = {}
    try:
        with open("cookies.txt", "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                key, value = line.split("=")
                cookies[key.strip()] = value.strip()
    except Exception as e:
        print("Cookies file read error:", e)
        exit()
    return cookies

cookies = load_cookies()

# Reaction Type (1=Like, 2=Love, 3=Care, 4=Haha, 7=Wow, 8=Sad, 16=Angry)
reaction_type = "2"  # Default: Love

# React on Posts
def react_on_post(post_id):
    try:
        url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={post_id}"
        response = requests.get(url, cookies=cookies)
        if "Reactions" in response.text:
            react_url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={post_id}&reaction_type={reaction_type}"
            requests.get(react_url, cookies=cookies)
            print(f"Reacted on Post: {post_id}")
    except Exception as e:
        print(f"Error reacting on Post {post_id}: {e}")

# React on Comments
def react_on_comment(comment_id):
    try:
        url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={comment_id}"
        response = requests.get(url, cookies=cookies)
        if "Reactions" in response.text:
            react_url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={comment_id}&reaction_type={reaction_type}"
            requests.get(react_url, cookies=cookies)
            print(f"Reacted on Comment: {comment_id}")
    except Exception as e:
        print(f"Error reacting on Comment {comment_id}: {e}")

# Load Post IDs
try:
    with open("post_ids.txt", "r") as f:
        post_ids = f.read().splitlines()
except:
    post_ids = []

# Load Comment IDs
try:
    with open("comment_ids.txt", "r") as f:
        comment_ids = f.read().splitlines()
except:
    comment_ids = []

# Start Reacting
for post in post_ids:
    react_on_post(post)
    time.sleep(2)  # Sleep to avoid rate limiting

for comment in comment_ids:
    react_on_comment(comment)
    time.sleep(2)

print("Auto react done!")
