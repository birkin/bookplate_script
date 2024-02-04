// use std::path::PathBuf;
// use regex::Regex;

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
