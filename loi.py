import requests
import os
import random
import time

# INDRA LOGO
INDRA_LOGO = """
 █████  ███    ██ ██████   █████  ██████  
██   ██ ████   ██ ██   ██ ██   ██ ██   ██ 
███████ ██ ██  ██ ██   ██ ███████ ██████  
██   ██ ██  ██ ██ ██   ██ ██   ██ ██   ██ 
██   ██ ██   ████ ██████  ██   ██ ██   ██ 
"""
print(INDRA_LOGO)

# Reaction Options
REACTIONS = {
    "1": "LIKE",
    "2": "LOVE",
    "3": "HAHA",
    "4": "WOW",
    "5": "SAD",
    "6": "ANGRY"
}

# Cookies file input
file_path = input("Enter your cookies file path: ")
if not os.path.exists(file_path):
    print("Error: File not found!")
    exit()

# Post ID input
post_id = input("Enter Post/Comment ID: ")

# Reaction Type Input
print("\nChoose Reaction Type:")
for key, value in REACTIONS.items():
    print(f"{key}: {value}")

reaction_choice = input("Enter choice (1-6): ")
reaction_type = REACTIONS.get(reaction_choice, "LIKE")

# Read Cookies File
with open(file_path, "r") as f:
    lines = f.read().splitlines()

# Auto React Function
def auto_react(cookies, c_user):
    try:
        # Reaction URL
        url = f"https://mbasic.facebook.com/ufi/reaction/?ft_ent_identifier={post_id}&reaction_type={reaction_choice}"
        
        # Request Headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Referer": f"https://mbasic.facebook.com/{post_id}"
        }

        # Send Reaction Request
        response = requests.get(url, cookies=cookies, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Reacted {reaction_type} from ID: {c_user}")
        else:
            print(f"❌ Failed to react from ID: {c_user}")

    except Exception as e:
        print(f"⚠ Error: {e}")

# Process Each Cookie
for line in lines:
    if "c_user" in line and "xs" in line:
        cookies = {}
        try:
            for part in line.split(";"):
                key, value = part.strip().split("=")
                cookies[key] = value
            
            c_user = cookies.get("c_user", "Unknown")
            auto_react(cookies, c_user)
            time.sleep(random.randint(3, 7))  # Random Delay to avoid detection
        except:
            print("⚠ Invalid Cookie Format:", line)

print("\nDone! All reactions sent.")
