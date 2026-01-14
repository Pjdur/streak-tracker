import datetime
import json
import os

DATA_FILE = "streak.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"streak": 0, "longest": 0, "last_date": None}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def check_in():
    data = load_data()
    today = str(datetime.date.today())

    # If last_date exists, compare with today
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
    save_data(data)

    print("=========================")
    print("   Coding Streak Tracker ")
    print("=========================")
    print(f"✅ Checked in for {today}")
    print(f"🔥 Current streak: {data['streak']} days")
    print(f"🏆 Longest streak: {data['longest']} days")

if __name__ == "__main__":
    check_in()
