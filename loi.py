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

# Facebook Cookies
cookies = {
    "c_user": "YOUR_C_USER",
    "xs": "YOUR_XS"
}

# Reaction Type (1=Like, 2=Love, 3=Care, 4=Haha, 7=Wow, 8=Sad, 16=Angry)
reaction_type = "2"  # Change as needed

def react_on_post(post_id):
    url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={post_id}"
    response = requests.get(url, cookies=cookies)
    if "Reactions" in response.text:
        react_url = f"https://mbasic.facebook.com/reactions/picker/?ft_id={post_id}&reaction_type={reaction_type}"
        requests.get(react_url, cookies=cookies)
        print(f"Reacted on post: {post_id}")

# Add your Post IDs here
post_ids = ["POST_ID_1", "POST_ID_2"]  # Add post IDs to react on

for post in post_ids:
    react_on_post(post)
    time.sleep(2)  # Sleep to avoid rate limiting

print("Auto react done!")
