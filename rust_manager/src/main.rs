use clap::{Parser, ArgAction};

/// This app runs different scripts based on the provided arguments
#[derive(Parser)]
#[command(version = "1.0", author = "Author Name <email@example.com>", about = "Describes what the app does")]
struct Args {
    /// Run report script
    #[arg(long, action = ArgAction::SetTrue)]
    report: bool,

    /// Run update script
    #[arg(long, action = ArgAction::SetTrue)]
    update: bool,

    /// Run both report and update scripts
    #[arg(long, action = ArgAction::SetTrue)]
    both: bool,
}

fn run_report() {
    println!("will generate report");
    // ...
}

fn run_daily_db_update() {
    println!("will update daily db");
    // ...
}

fn main() {
    let args = Args::parse();

    if !args.report && !args.update && !args.both {
        println!("Please provide either the --update, --report, or --both argument.");
        std::process::exit(1);
    }

    if args.report || args.both {
        run_report();
    }
    if args.update || args.both {
        run_daily_db_update();
    }
}
