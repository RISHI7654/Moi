import requests
import os
import random
import time

# INDRA LOGO
INDRA_LOGO = """
  /$$$$$$ /$$   /$$ /$$$$$$$  /$$$$$$$   /$$$$$$ 
|_  $$_/| $$$ | $$| $$__  $$| $$__  $$ /$$__  $$
  | $$  | $$$$| $$| $$  \ $$| $$  \ $$| $$  \ $$
  | $$  | $$ $$ $$| $$  | $$| $$$$$$$/| $$$$$$$$
  | $$  | $$  $$$$| $$  | $$| $$__  $$| $$__  $$
  | $$  | $$\  $$$| $$  | $$| $$  \ $$| $$  | $$
 /$$$$$$| $$ \  $$| $$$$$$$/| $$  | $$| $$  | $$
|______/|__/  \__/|_______/ |__/  |__/|__/  |__/                                                                                                            
"""
print(INDRA_LOGO)

# Poll Vote Options
POLL_VOTE_OPTIONS = {
    "1": "Vote using ID",
    "2": "Vote using Page UID",
    "3": "Vote using both ID and Page UID"
}

# Cookies file input
file_path = input("Enter your cookies file path: ")
if not os.path.exists(file_path):
    print("Error: File not found!")
    exit()

# Poll ID input
poll_id = input("Enter Poll ID: ")

# Poll Vote Option Input
print("\nChoose Poll Vote Option:")
for key, value in POLL_VOTE_OPTIONS.items():
    print(f"{key}: {value}")

vote_choice = input("Enter choice (1-3): ")

# Read Cookies File
with open(file_path, "r") as f:
    lines = f.read().splitlines()

# Poll Vote Function
def poll_vote(cookies, c_user, vote_type):
    try:
        if vote_type == "ID":
            # Poll vote using ID
            url = f"https://mbasic.facebook.com/ufi/reaction/?ft_ent_identifier={poll_id}&reaction_type=1"

        elif vote_type == "Page":
            # Poll vote using Page UID
            url = f"https://mbasic.facebook.com/{poll_id}/reaction/?reaction_type=1&page_id=PAGE_UID"

        elif vote_type == "Both":
            # Poll vote using both ID and Page UID
            url = f"https://mbasic.facebook.com/{poll_id}/reaction/?reaction_type=1&page_id=PAGE_UID&user_id={c_user}"

        # Request Headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Referer": f"https://mbasic.facebook.com/{poll_id}"
        }

        # Send Poll Vote Request
        response = requests.get(url, cookies=cookies, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Voted from ID: {c_user}")
        else:
            print(f"❌ Failed to vote from ID: {c_user}")

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
            
            # Poll voting based on user choice
            if vote_choice == "1":
                poll_vote(cookies, c_user, "ID")
            elif vote_choice == "2":
                poll_vote(cookies, c_user, "Page")
            elif vote_choice == "3":
                poll_vote(cookies, c_user, "Both")
            
            time.sleep(random.randint(3, 7))  # Random Delay to avoid detection
        except:
            print("⚠ Invalid Cookie Format:", line)

print("\nDone! All votes sent.")
