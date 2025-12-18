import requests
import time
from datetime import datetime
from termcolor import colored

# Update to reflect your "Otonashi" branding
OTONASHI_LOGO = """

██████╗  ██████╗ ██████╗ ██╗      ██████╗ ██╗  ██╗    ██╗███╗   ██╗███████╗ ██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██║     ██╔═══██╗╚██╗██╔╝    ██║████╗  ██║██╔════╝██╔═══██╗
██████╔╝██║   ██║██████╔╝██║     ██║   ██║ ╚███╔╝     ██║██╔██╗ ██║█████╗  ██║   ██║
██╔══██╗██║   ██║██╔══██╗██║     ██║   ██║ ██╔██╗     ██║██║╚██╗██║██╔══╝  ██║   ██║
██║  ██║╚██████╔╝██████╔╝███████╗╚██████╔╝██╔╝ ██╗    ██║██║ ╚████║██║     ╚██████╔╝
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
                                                                                    
"""

print(colored(OTONASHI_LOGO, "cyan", attrs=["bold"]))
print(colored("            Created by Otonashi\n", "yellow", attrs=["bold"]))

def parse_date(date_str):
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return "Unknown Date"

def get_roblox_user_info(username, password):
    try:
        user_lookup_url = "https://users.roblox.com/v1/usernames/users"
        response = requests.post(user_lookup_url, json={"usernames": [username]})
        response.raise_for_status()
        user_data = response.json().get("data", [])[0]
        user_id = user_data["id"]

        profile = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get("count", 0)
        followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get("count", 0)
        badges = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100").json().get("data", [])
        groups = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles").json()
        collectibles = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=10").json().get("data", [])
        avatar = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png"

        return {
            "USER": username,
            "PASS": password,
            "UserID": user_id,
            "Username": profile.get("name"),
            "DisplayName": profile.get("displayName"),
            "ProfileURL": f"https://www.roblox.com/users/{user_id}/profile",
            "Description": profile.get("description", "N/A"),
            "IsBanned": profile.get("isBanned", False),
            "AccountAgeDays": profile.get("age"),
            "JoinDate": parse_date(profile.get("created")),
            "BadgeCount": len(badges),
            "CollectibleCount": len(collectibles),
            "GroupCount": len(groups),
            "FriendCount": friends,
            "FollowerCount": followers,
            "Avatar": avatar
        }

    except Exception as e:
        print(colored(f"❌ Error fetching {username}: {e}", "red", attrs=["bold"]))
        return None

file_name = input("Enter file name: ")

try:
    with open(file_name, "r") as file:
        lines = file.read().splitlines()

    accounts = []

    print(colored("\n🚀 Fetching data...\n", "yellow", attrs=["bold"]))
    for line in lines:
        try:
            username, password = line.split(":", 1)
            username, password = username.strip(), password.strip()
            if username and password:
                accounts.append((username, password))
            else:
                print(colored(f"❌ Skipping invalid entry: {line}", "red", attrs=["bold"]))
        except ValueError:
            print(colored(f"❌ Invalid format: {line}", "red", attrs=["bold"]))

    output_file_name = "Roblox_results.txt"
    with open(output_file_name, "w") as output_file:
        output_file.write(colored(Otonashi_LOGO, "cyan", attrs=["bold"]) + "\n")
        output_file.write(colored("            Created by Otonashi", "yellow", attrs=["bold"]) + "\n\n")

        for index, (username, password) in enumerate(accounts, start=1):
            print(colored(f"🔍 Checking {index}/{len(accounts)}: {username}...", "yellow", attrs=["bold"]))
            info = get_roblox_user_info(username, password)
            if info:
                output_file.write(colored("⪻━━━━━═『Roblox Info』═━━━━━⪼", "cyan", attrs=["bold"]) + "\n\n")
                for key, val in info.items():
                    output_file.write(f"[+] {key}: {val}\n")
                    print(colored(f"[+] {key}: {val}", "green", attrs=["bold"]))  # real-time output in green
                output_file.write("\n⪻━━━━━━━━━━━━━━━━━━━⪼\n\n")
                print(colored("⪻━━━━━━━━━━━━━━━━━━━⪼", "cyan", attrs=["bold"]) + "\n")
            else:
                print(colored(f"❌ Failed to fetch info for: {username}", "red", attrs=["bold"]))
            time.sleep(0.1)

    print(colored(f"\n✅ Done! Results saved in '{output_file_name}'.", "green", attrs=["bold"]))

except FileNotFoundError:
    print(colored("❌ Error: File not found!", "red", attrs=["bold"]))
except Exception as e:
    print(colored(f"❌ Unexpected error: {e}", "red", attrs=["bold"]))