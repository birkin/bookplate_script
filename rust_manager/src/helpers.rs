pub fn sort_files( unsorted_files: Vec<std::path::PathBuf> ) -> Vec<std::path::PathBuf> {
    let mut sorted_files: Vec<std::path::PathBuf> = unsorted_files;
    sorted_files.sort();
    sorted_files
}