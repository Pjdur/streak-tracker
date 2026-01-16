import datetime
import json
import os
import argparse

# Save streak.json in the user's home directory
HOME_DIR = os.path.expanduser("~")
DATA_FILE = os.path.join(HOME_DIR, "streak.json")

BADGES = {
    7: "🥉 7-day streak badge unlocked!",
    30: "🥈 30-day streak badge unlocked!",
    100: "🥇 100-day streak badge unlocked!",
    365: "🏆 1-year streak badge unlocked!"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        # Create the file with default data if it doesn't exist
        data = {"streak": 0, "longest": 0, "last_date": None, "history": []}
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def print_weekly_line(history):
    # Show last 7 days streak line
    today = datetime.date.today()
    days = ["M","T","W","T","F","S","S"]
    line = ""
    markers = ""
    for i in range(7):
        day = today - datetime.timedelta(days=(6-i))
        if str(day) in history:
            line += "● "  # filled dot
        else:
            line += "○ "  # empty dot
        markers += days[day.weekday()] + " "
    print(line.strip())
    print(markers.strip())

def check_in():
    data = load_data()
    today = str(datetime.date.today())

    if data["last_date"]:
        last_date = datetime.date.fromisoformat(data["last_date"])
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        if last_date == yesterday:
            data["streak"] += 1
        elif last_date == datetime.date.today():
            print("You already checked in today!")
            return
        else:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today
    data["longest"] = max(data["longest"], data["streak"])
    if today not in data["history"]:
        data["history"].append(today)
    save_data(data)

    print("=========================")
    print("   Coding Streak Tracker ")
    print("=========================")
    print(f"✅ Checked in for {today}")
    print(f"🔥 Current streak: {data['streak']} days")
    print(f"🏆 Longest streak: {data['longest']} days")

    # Badge unlocks
    if data["streak"] in BADGES:
        print(BADGES[data["streak"]])

    # Weekly streak line
    print("\n📅 This week’s streak:")
    print_weekly_line(data["history"])

def show_status():
    data = load_data()
    print("=========================")
    print("   Coding Streak Tracker ")
    print("=========================")
    print(f"🔥 Current streak: {data['streak']} days")
    print(f"🏆 Longest streak: {data['longest']} days")
    print("\n📅 This week’s streak:")
    print_weekly_line(data["history"])

def show_history():
    data = load_data()
    print("=========================")
    print("   Coding Streak Tracker ")
    print("=========================")
    print("📜 Check-in history:")

    if not data["history"]:
        print("No check-ins yet.")
    else:
        for date in data["history"]:
            print(date)

def main():
    parser = argparse.ArgumentParser(description="Coding Streak Tracker")
    parser.add_argument("action", choices=["checkin", "status", "week", "history"], nargs="?", default="checkin",
                        help="Choose an action: checkin, status, week, or history")
    args = parser.parse_args()

    if args.action == "checkin":
        check_in()
    elif args.action == "status":
        show_status()
    elif args.action == "week":
        data = load_data()
        print_weekly_line(data["history"])
    elif args.action == "history":
        show_history()

if __name__ == "__main__":
    main()
