// use std::collections::HashMap;
use std::collections::BTreeMap;
use std::fs::File;
use std::io::BufReader;
use std::io::Read;

use serde::Deserialize;

/*
Structs to represent MARC XML structure -----------------------------
*/

#[derive(Debug, Deserialize)]
pub struct Collection {
    #[serde(rename = "record", default)]
    pub records: Vec<RecordXml>,
}

#[derive(Debug, Deserialize)]
pub struct RecordXml {
    #[serde(rename = "controlfield", default)]
    controlfields: Vec<ControlField>,
    #[serde(rename = "datafield", default)]
    datafields: Vec<DataField>,
}

#[derive(Debug, Deserialize)]
struct ControlField {
    #[serde(rename = "tag")]
    tag: String,
    #[serde(rename = "$value")]
    value: Option<String>,
}

#[derive(Debug, Deserialize)]
struct DataField {
    #[serde(rename = "tag")]
    tag: String,
    // #[serde(rename = "ind1")]
    // ind1: String,
    // #[serde(rename = "ind2")]
    // ind2: String,
    #[serde(rename = "subfield", default)]
    subfields: Vec<SubField>,
}

#[derive(Debug, Deserialize)]
struct SubField {
    #[serde(rename = "code")]
    code: String,
    #[serde(rename = "$value")]
    // value: String,
    value: Option<String>,
}

// end of structs ---------------------------------------------------

pub fn load_records(marc_xml_path: &str) -> Collection {
    /*
    Read the MARC XML file into a string, then deserialize it via serde-xml-rs, using the Collection struct.
    */

    //- open file -------------------------------
    let file = File::open(marc_xml_path).unwrap_or_else(|err| {
        panic!("could not open the marc_xml_path; error, ``{}``", err);
    });

    //- read to string --------------------------
    let mut reader = BufReader::new(file);
    let mut contents = String::new();
    // reader.read_to_string(&mut contents)?;
    reader.read_to_string(&mut contents).unwrap_or_else(|err| {
        panic!("could not read the file; error, ``{}``", err);
    });

    //- Deserialize XML to Collection -----------
    let collection: Collection = serde_xml_rs::from_str(&contents).unwrap_or_else(|err| {
        panic!("could not deserialize the marc_xml; error, ``{}``", err);
    });

    //- log the collection ----------------------
    let collection_str = format!("{:?}", collection);
    let collection_substr_ellipses = format!("{}...", &collection_str[..collection_str.len().min(200)]);
    log_debug!("collection (partial), ``{:?}``", collection_substr_ellipses);

    return collection;
}

// pub fn process_record(record: &RecordXml) -> HashMap<String, String> {
//     /*
//     Extracts any bookplate info from the record.
//     Returns a HashMap with the following keys:
//     - bookplate_996_u_info
//     - bookplate_996_z_info
//     - mms_id
//     - title
//     */
//     let bookplate_996_u_info: String = parse_996_u(&record);
//     let mut data = HashMap::new();

//     if bookplate_996_u_info != "" {
//         let bookplate_996_z_info: String = parse_996_z(&record);
//         let mms_id: String = parse_alma_mmsid(&record);
//         let title: String = parse_title(&record); // Not needed for work, helps humans
//         log_debug!("bookplate info found");
//         data.insert("bookplate_996_u_info".to_string(), bookplate_996_u_info);
//         data.insert("bookplate_996_z_info".to_string(), bookplate_996_z_info);
//         data.insert("mms_id".to_string(), mms_id);
//         data.insert("title".to_string(), title);
//     } else {
//         log_debug!("no bookplate info found");
//     }

//     data
// }

pub fn process_record(record: &RecordXml) -> BTreeMap<String, String> {
    /*
    Extracts any bookplate info from the record.
    Returns a HashMap with the following keys:
    - bookplate_996_u_info
    - bookplate_996_z_info
    - mms_id
    - title
    */
    let bookplate_996_u_info: String = parse_996_u(&record);
    let mut data = BTreeMap::new();

    if bookplate_996_u_info != "" {
        let bookplate_996_z_info: String = parse_996_z(&record);
        let mms_id: String = parse_alma_mmsid(&record);
        let title: String = parse_title(&record); // Not needed for work, helps humans
        log_debug!("bookplate info found");
        data.insert("bookplate_996_u_info".to_string(), bookplate_996_u_info);
        data.insert("bookplate_996_z_info".to_string(), bookplate_996_z_info);
        data.insert("mms_id".to_string(), mms_id);
        data.insert("title".to_string(), title);
    } else {
        log_debug!("no bookplate info found");
    }

    data
}

fn parse_996_u(record: &RecordXml) -> String {
    /*
    Checks 996-u for bookplate text and returns it if found.
    If not found, returns empty string.
    */
    let mut the_996_u = String::new();
    for datafield in &record.datafields {
        if datafield.tag == "996" {
            for subfield in &datafield.subfields {
                if subfield.code == "u" {
                    let subfield_text = subfield.value.clone().unwrap_or_else(|| "".to_string());
                    if subfield_text.to_lowercase().contains("bookplate") {
                        the_996_u = subfield_text;
                    }
                }
            }
        }
    }
    the_996_u
}

fn parse_996_z(record: &RecordXml) -> String {
    /*
    Thus function is only called when the previous `parse_996_u()` function has found bookplate info.
    Grabs the 996-z for "purchased with fund" text.
    */
    let mut the_996_z = String::new();
    for datafield in &record.datafields {
        if datafield.tag == "996" {
            for subfield in &datafield.subfields {
                if subfield.code == "z" {
                    the_996_z = subfield.value.clone().unwrap_or_else(|| "".to_string());
                }
            }
        }
    }
    the_996_z
}

fn parse_alma_mmsid(record: &RecordXml) -> String {
    let mut alma_mmsid = String::new();
    for controlfield in &record.controlfields {
        if controlfield.tag == "001" {
            alma_mmsid = controlfield.value.clone().unwrap_or_else(|| "".to_string());
        }
    }
    alma_mmsid
}

fn parse_title(record: &RecordXml) -> String {
    let mut title = String::new();
    for datafield in &record.datafields {
        if datafield.tag == "245" {
            for subfield in &datafield.subfields {
                if subfield.code == "a" {
                    title = subfield.value.clone().unwrap_or_else(|| "".to_string());
                    // title explanation: <https://gist.github.com/birkin/57952fa4052167ddb8b5c98ec8beb920>
                }
            }
        }
    }
    title
}

/*
Dummy function for testing ------------------------------------------
*/
// fn add_nums(a: i32, b: i32) -> i32 {
//     a + b
// }

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_add_nums() {
//         let expected = 3;
//         let result = add_nums(1, 2);
//         assert_eq!(result, expected);
//     }
// }
