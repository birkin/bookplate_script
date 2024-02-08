// use std::collections::HashMap;
// use std::io::BufRead;
// use std::io::BufReader;
use flate2::read::GzDecoder;
use regex::Regex;
use std::fs::{self, File};
use std::io::Result;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use tar::Archive;

// const RECORD_TERMINATOR: u8 = 0x1D;

pub fn grab_directory_files(directory: &str) -> Vec<std::path::PathBuf> {
    /*
    Some notes...
    - ```std::fs::read_dir(marc_full_source_files_dir)```
            Returns a Result, which means an Ok or an Err.
            The order of directory entries not 'sorted' -- it's generally optimized for the filesystem's (e.g., NTFS, FAT, ext4, etc.) performance and organization,
            rather than for human-readable sorting or any specific application-level need.
    - ```let entry = entry.expect("Error reading entry");```
            This is a way to handle the Result returned by read_dir.
            If the Result is an Err, the program will panic with the message "Error reading entry".
            If the Result is an Ok, the program will continue with the value of the Ok.
    - This could be one long dot-chained line, like:
            std::fs::read_dir(directory)
            .expect("Unable to read directory")
            .map(|res| res.map(|e| e.path()))
            .collect::<Result<Vec<_>, std::io::Error>>()
            .expect("Unable to collect files")
        ...but that hurts my brain.
    */
    let entries = std::fs::read_dir(directory).expect("Unable to read directory");
    let mut paths = Vec::new();
    for entry in entries {
        // entry is `Result<DirEntry, std::io::Error>`
        let entry: std::fs::DirEntry = entry.expect("Error reading entry");
        paths.push(entry.path());
    }
    log_debug!("first 3 unsorted_compressed_marc_files: {:?}", &paths[0..3]);

    return paths;
}

pub fn sort_files(mut unsorted_files: Vec<PathBuf>) -> Vec<PathBuf> {
    /*
    Sorts a list of filename path-objects that have unpadded numbers.
    Without padding, a simple-sort via string would yield entries like this: 1, 10, 100, 2, 20, 200, 3, 30, 300, etc.
    The sort_by() method sorts the items in-place.
    */
    // regex to find the numeric part of the filename
    let re = Regex::new(r"\d+").unwrap();
    // sort away...
    unsorted_files.sort_by(|a, b| {
        // extract the stem as a &str, or use empty string if none. The stem actually still has the .tar extension, but that doesn't matter for the sort
        let stem_a: &str = a.file_stem().and_then(|s| s.to_str()).unwrap_or("");
        let stem_b: &str = b.file_stem().and_then(|s| s.to_str()).unwrap_or("");
        // use regex to find the first numeric part of each stem
        let num_a: i32 = re.find(stem_a).and_then(|m| m.as_str().parse::<i32>().ok()).unwrap_or(0);
        let num_b: i32 = re.find(stem_b).and_then(|m| m.as_str().parse::<i32>().ok()).unwrap_or(0);
        // compare by the numeric part
        num_a
            .cmp(&num_b)
            // if numeric parts are equal, fall back to comparing the whole stem lexically
            .then_with(|| stem_a.cmp(stem_b))
    });
    log_info!(
        "found ``{:?}`` marc files in ``{:?}``",
        &unsorted_files.len(),
        &unsorted_files[0].parent().expect("unable to get parent directory")
    );
    log_debug!(
        "first 3 sorted_compressed_marc_files: ``{:?}``",
        &unsorted_files[0..3]
    );

    unsorted_files // Vec<PathBuf> -- and they're now sorted
}

pub fn extract_tar_gz(archive_path: &PathBuf, output_dir: &str) -> Result<PathBuf> {
    /*
    - Extracts a .tar.gz file to a directory,
    - Sets the file to be group read-writeable,
    - Returns the path to the extracted file
    */
    // Open file
    let f = File::open(archive_path)?; // Propagate error to caller
    let decoder = GzDecoder::new(f);
    // Create a new archive object
    let mut archive = Archive::new(decoder);
    // Unpack the archive's contents into the output directory
    archive.unpack(output_dir)?; // Propagate error to caller

    // Construct the output file name
    let file_stem = archive_path
        .file_stem() // Get the file stem (filename without the last extension)
        .and_then(|f| f.to_str()) // Convert OsStr to &str
        .map(|s| s.trim_end_matches(".tar")) // Trim the ".tar" part if it exists
        .unwrap_or(""); // Fallback to empty string if any step fails

    let output_file_name = format!("{}.xml", file_stem); // Append ".xml" to the file stem

    // Construct the full path to the output file
    let output_path = Path::new(output_dir).join(output_file_name);

    // Set group permissions to read-write
    let metadata = fs::metadata(&output_path)?;
    let mut permissions = metadata.permissions();
    permissions.set_mode(0o664); // rw-rw-r--: Owner and group have read-write, others have read
    fs::set_permissions(&output_path, permissions)?;

    Ok(output_path)
}
