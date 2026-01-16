use std::fs;
use std::path::PathBuf;
use serde::{Serialize, Deserialize};
use chrono::prelude::*;
use clap::Parser;

fn maybe_show_badge(streak: u32) {
    match streak {
        7 => println!("🥉 7-day streak badge unlocked!"),
        30 => println!("🥈 30-day streak badge unlocked!"),
        100 => println!("🥇 100-day streak badge unlocked!"),
        365 => println!("🏆 1-year streak badge unlocked!"),
        _ => {}
    }
}

fn data_file_path() -> PathBuf {
    let mut home = dirs::home_dir().expect("Could not find home directory");
    home.push("streak.json");
    home
}

#[derive(Serialize, Deserialize)]
struct StreakData {
    streak: u32,
    longest: u32,
    last_date: Option<String>,
    history: Vec<String>
}

fn load_data() -> Result<StreakData, std::io::Error> {
    let data_file = data_file_path();
    if data_file.exists() {
        let data = fs::read_to_string(data_file)?;
        Ok(serde_json::from_str(&data)?)
    } else {
        Ok(StreakData {
            streak: 0,
            longest: 0,
            last_date: None,
            history: Vec::new()
        })
    }
}

fn save_data(data: &StreakData) -> Result<(), std::io::Error> {
    let data_file = data_file_path();
    let data_str = serde_json::to_string_pretty(data)?;
    fs::write(data_file, data_str)?;
    Ok(())
}

fn checkin() -> Result<(), Box<dyn std::error::Error>> {
    let today = Local::now().date_naive().to_string();
    let mut data = load_data()?;

    if let Some(last) = &data.last_date {
        let last_date = NaiveDate::parse_from_str(last, "%Y-%m-%d")?;
        let yesterday = Local::now().date_naive() - chrono::Duration::days(1);

        if last_date == yesterday {
            data.streak += 1;
        } else if last_date == Local::now().date_naive() {
            println!("You already checked in today!");
            return Ok(());
        } else {
            data.streak = 1;
        }
    } else {
        data.streak = 1;
    }

    data.last_date = Some(today.clone());
    if !data.history.contains(&today) {
        data.history.push(today.clone());
    }
    if data.streak > data.longest {
        data.longest = data.streak;
    }

    save_data(&data)?;

    println!("=========================");
    println!("   Coding Streak Tracker ");
    println!("=========================");
    println!("✅ Checked in for {}", today);
    println!("🔥 Current streak: {} days", data.streak);
    println!("🏆 Longest streak: {} days", data.longest);
    maybe_show_badge(data.streak);
    Ok(())
}

fn print_weekly_line(history: &[String]) {
    let today = Local::now().date_naive();
    let days = ["M","T","W","T","F","S","S"];

    let mut line = String::new();
    let mut markers = String::new();

    for i in 0..7 {
        let day = today - chrono::Duration::days((6 - i) as i64);
        let day_str = day.to_string();

        if history.contains(&day_str) {
            line.push_str("● ");
        } else {
            line.push_str("○ ");
        }

        let weekday_index = day.weekday().num_days_from_monday() as usize;
        markers.push_str(days[weekday_index]);
        markers.push(' ');
    }

    println!("{}", line.trim());
    println!("{}", markers.trim());
}

fn show_status() -> Result<(), Box<dyn std::error::Error>> {
    let data = load_data()?;

    println!("=========================");
    println!("   Coding Streak Tracker ");
    println!("=========================");
    println!("🔥 Current streak: {} days", data.streak);
    println!("🏆 Longest streak: {} days", data.longest);

    println!("\n📅 This week’s streak:");
    print_weekly_line(&data.history);

    Ok(())
}

fn show_history() -> Result<(), Box<dyn std::error::Error>> {
    let data = load_data()?;

    println!("=========================");
    println!("   Coding Streak Tracker ");
    println!("=========================");
    println!("📜 Check-in history:");

    if data.history.is_empty() {
        println!("No check-ins yet.");
    } else {
        for date in &data.history {
            println!("{}", date);
        }
    }

    Ok(())
}

#[derive(Parser)]
struct Cli {
    action: Option<String>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    match cli.action.as_deref() {
        Some("checkin") | None => checkin()?,
        Some("status") => show_status()?,
        Some("week") => {
            let data = load_data()?;
            print_weekly_line(&data.history);
        }
        Some("history") => show_history()?,
        Some(other) => println!("Unknown action: {}", other),
    }
    Ok(())
}
