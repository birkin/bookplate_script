
pub fn grab_direcory_files(directory: &str) -> Vec<std::path::PathBuf> {
    /*  Some notes...
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
        let entry = entry.expect("Error reading entry");
        paths.push(entry.path());
    }
    return paths;
}

pub fn sort_files(unsorted_files: Vec<std::path::PathBuf>) -> Vec<std::path::PathBuf> {
    let mut sorted_files: Vec<std::path::PathBuf> = unsorted_files;
    sorted_files.sort();
    sorted_files
}

// pub fn sort_files(mut unsorted_files: Vec<PathBuf>) -> Vec<PathBuf> {
//     // Compile a regex to find the numeric part of the filename
//     let re = Regex::new(r"\d+").unwrap();

//     unsorted_files.sort_by(|a, b| {
//         // Extract the stem (filename without extension) as a &str, or use empty string if none
//         let stem_a = a.file_stem().and_then(|s| s.to_str()).unwrap_or("");
//         let stem_b = b.file_stem().and_then(|s| s.to_str()).unwrap_or("");

//         // Use regex to find the first numeric part of each stem
//         let num_a = re.find(stem_a).and_then(|m| m.as_str().parse::<i32>().ok()).unwrap_or(0);
//         let num_b = re.find(stem_b).and_then(|m| m.as_str().parse::<i32>().ok()).unwrap_or(0);

//         // First compare by the numeric part
//         num_a.cmp(&num_b)
//             // If numeric parts are equal, fall back to comparing the whole stem lexically
//             .then_with(|| stem_a.cmp(stem_b))
//     });

//     unsorted_files
// }