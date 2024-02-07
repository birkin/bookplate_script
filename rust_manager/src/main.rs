// use std::collections::HashMap;
use clap::{ArgAction, Parser};
use dotenvy::dotenv;
use std::env;

#[macro_use]
mod logger; // enables the log_debug!() and log_info!() macros; needs to be before the other modules that use it

mod helpers;
mod marc_xml_reader;

/*
    Includes the file generated by the build.rs script, which looks like:
    pub const GIT_COMMIT: &str = "c5f7034f79bc3d49c1a9fb81c7cac6a8a778c5c3";
*/
include!(concat!(env!("OUT_DIR"), "/git_commit.rs"));

// - argument-handling ----------------------------------------------
#[derive(Parser)]
#[command(
    // version = "1.0",
    version = GIT_COMMIT,
    author = "Author Name <email@example.com>",
    about = "Runs \"update\" or \"report\" bookplate-scripts based on the provided arguments."
)]
struct Args {
    #[arg(long, action = ArgAction::SetTrue)]
    report: bool,
    #[arg(long, action = ArgAction::SetTrue)]
    update: bool,
    #[arg(long, action = ArgAction::SetTrue)]
    both: bool,
} // end argument-handling ------------------------------------------

/*
main ------------------------------------------------------------
*/
fn main() {
    // - load envars ------------------------------------------------
    dotenv().ok();
    let _marc_daily_source_files_dir: String = env::var("MARC_DAILY_SOURCE_DIR")
        .expect("MARC_DAILY_SOURCE_DIR envar could not be retrieved.");
    let marc_full_source_files_dir: String = env::var("MARC_FULL_SOURCE_DIR")
        .expect("MARC_FULL_SOURCE_DIR envar could not be retrieved.");
    let marc_full_output_files_dir: String = env::var("MARC_FULL_OUTPUT_DIR")
        .expect("MARC_FULL_OUTPUT_DIR envar could not be retrieved.");

    // - set up logger ----------------------------------------------
    logger::init_logger().expect("Unable to initialize logger");
    log_debug!("logging configured.");

    // - parse args --------------------------------------------------
    let args = Args::parse();
    if !args.report && !args.update && !args.both {
        println!("Please provide either the --update, --report, or --both argument.");
        std::process::exit(1);
    }

    // - run scripts ------------------------------------------------
    if args.report || args.both {
        run_report(&marc_full_source_files_dir, &marc_full_output_files_dir);
    }
    if args.update || args.both {
        run_daily_db_update();
    }
}

/*
manage report-run ---------------------------------------------------
*/
fn run_report(marc_full_source_files_dir: &str, marc_full_output_files_dir: &str) {
    log_debug!("marc_full_output_files_dir: {}", marc_full_output_files_dir); // temp; to eliminate cargo warning

    // list the .tar.gz files -------------------
    let unsorted_compressed_marc_files: Vec<std::path::PathBuf> =
        helpers::grab_directory_files(&marc_full_source_files_dir);

    // get a sorted list ------------------------
    let compressed_marc_files: Vec<std::path::PathBuf> =
        helpers::sort_files(unsorted_compressed_marc_files);

    // loop through list ------------------------
    for (i, file) in compressed_marc_files.iter().enumerate() {
        log_debug!("processing file: {:?}", file);

        // decompress & write file --------------
        let output_file: std::path::PathBuf =
            helpers::extract_tar_gz(&file, marc_full_output_files_dir)
                .unwrap_or_else(|_| panic!("Problem extracting file: {:?}", file.display())); // possible TODO: log and/or email error, but continue processing.
        log_debug!("output_file: {:?}", &output_file);

        // read marc-xml file -------------------
        /*
        - open file
        - create a list of marc-records
        - for all marc-records, pull out title
         */
        // let _bookplate_data: Vec<HashMap<std::string::String, std::string::String>> =
        //     helpers::read_marc_xml(&output_file);

        // delete file ---------------------------

        // Log progress for every fifth file, i starts at 0 so add 1 for human-readable count
        if (i + 1) % 3 == 0 {
            log_info!(
                "Processed {} of {} files.",
                i + 1,
                compressed_marc_files.len()
            );
        }

        if i >= 4 {
            break; // break after processing subset of files
        }
    }

    log_info!("done");
} // end run_report()

/*
manage daily-db-update ----------------------------------------------
*/
fn run_daily_db_update() {
    println!("will update daily db");
    // ...
}

/*
for reference: using rayon ------------------------------------------
*/
// fn run_report(marc_full_source_files_dir: &str, marc_full_output_files_dir: &str) {
//     log_debug!("marc_full_output_files_dir: {}", marc_full_output_files_dir);

//     let unsorted_compressed_marc_files: Vec<std::path::PathBuf> =
//         helpers::grab_directory_files(marc_full_source_files_dir);

//     let compressed_marc_files: Vec<std::path::PathBuf> =
//         helpers::sort_files(unsorted_compressed_marc_files);

//     // Create a subset of the first 10 items (or fewer, if there aren't 10)
//     let subset_compressed_marc_files: Vec<&std::path::PathBuf> =
//         compressed_marc_files.iter().take(10).collect();

//     // Use Rayon's parallel iterator to process the subset in parallel
//     subset_compressed_marc_files.par_iter().for_each(|file| {
//         log_debug!("processing file: {:?}", file);
//         helpers::extract_tar_gz(file, marc_full_output_files_dir)
//             .unwrap_or_else(|_| panic!("Problem extracting file: {:?}", file.display()));
//     });

//     log_info!("done");
// }
