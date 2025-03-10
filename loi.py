import requests
import os
import random
import time
from bs4 import BeautifulSoup  # Install this library: pip install beautifulsoup4

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
    "2": "Vote using Page UID (for pages linked with the user ID)"
}

# Cookies file input
file_path = input("Enter your cookies file path: ")
if not os.path.exists(file_path):
    print("Error: File not found!")
    exit()

# Post ID input
post_id = input("Enter Post ID (the ID of the post containing the polls): ")

# Poll Vote Option Input
print("\nChoose Poll Vote Option:")
for key, value in POLL_VOTE_OPTIONS.items():
    print(f"{key}: {value}")

vote_choice = input("Enter choice (1-2): ")

# Read Cookies File
with open(file_path, "r") as f:
    lines = f.read().splitlines()

# Poll Vote Function
def poll_vote(cookies, c_user, poll_id, page_uid=None):
    try:
        if vote_choice == "1":
            # Poll vote using User ID's cookies
            url = f"https://mbasic.facebook.com/ufi/reaction/?ft_ent_identifier={poll_id}&reaction_type=1"

        elif vote_choice == "2" and page_uid:
            # Poll vote using Page UID associated with User ID's cookies
            url = f"https://mbasic.facebook.com/{poll_id}/reaction/?reaction_type=1&page_id={page_uid}"

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

# Extracting page UIDs linked to user (this part depends on the user’s pages)
def get_page_uids(cookies, c_user):
    page_uids = []
    try:
        # Make a request to Facebook to fetch pages linked to the user
        url = f"https://mbasic.facebook.com/{c_user}/pages"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Referer": f"https://mbasic.facebook.com/{c_user}/pages"
        }

        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code == 200:
            # Here you should parse the page UIDs from the response
            # For simplicity, assume you get page UIDs here:
            page_uids = ["PAGE_UID_1", "PAGE_UID_2"]  # Replace with actual parsing logic
        else:
            print(f"⚠ Failed to fetch pages for user {c_user}")
    except Exception as e:
        print(f"⚠ Error fetching pages: {e}")
    return page_uids

# Fetch Polls from a Post
def get_polls_from_post(post_id, cookies):
    polls = []
    try:
        # Send a request to the post
        url = f"https://mbasic.facebook.com/{post_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Referer": f"https://mbasic.facebook.com/{post_id}"
        }

        response = requests.get(url, cookies=cookies, headers=headers)
        
        if response.status_code == 200:
            # Use BeautifulSoup to parse the HTML and find poll IDs
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all polls (assuming they have a specific HTML structure)
            for poll in soup.find_all("a", href=True):
                # Check if this link contains a poll ID
                if 'reaction' in poll['href']:
                    poll_id = poll['href'].split('=')[1]  # Example extraction, adjust based on actual structure
                    polls.append(poll_id)

        else:
            print(f"⚠ Failed to fetch post {post_id}")

    except Exception as e:
        print(f"⚠ Error fetching polls: {e}")
    return polls

# Process Each Cookie
for line in lines:
    if "c_user" in line and "xs" in line:
        cookies = {}
        try:
            for part in line.split(";"):
                key, value = part.strip().split("=")
                cookies[key] = value
            
            c_user = cookies.get("c_user", "Unknown")

            # Fetch Polls from the Post
            polls = get_polls_from_post(post_id, cookies)
            if polls:
                print("\nAvailable Polls in the Post:")
                for idx, poll_id in enumerate(polls, 1):
                    print(f"{idx}. Poll ID: {poll_id}")
                
                poll_choice = int(input("Choose which Poll ID you want to vote on (1-N): ")) - 1
                if 0 <= poll_choice < len(polls):
                    chosen_poll_id = polls[poll_choice]
                    print(f"Voting on Poll ID: {chosen_poll_id}")
                    # Fetch Pages Linked to User (Page UID's)
                    page_uids = get_page_uids(cookies, c_user)
                    
                    # Poll voting based on user choice
                    if vote_choice == "1":
                        poll_vote(cookies, c_user, chosen_poll_id)
                    elif vote_choice == "2" and page_uids:
                        for page_uid in page_uids:
                            poll_vote(cookies, c_user, chosen_poll_id, page_uid)
                else:
                    print("⚠ Invalid poll choice.")
            
            time.sleep(random.randint(3, 7))  # Random Delay to avoid detection

        except:
            print("⚠ Invalid Cookie Format:", line)

print("\nDone! All votes sent.")
