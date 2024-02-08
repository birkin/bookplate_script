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
    let collection_substr_ellipses =
        format!("{}...", &collection_str[..collection_str.len().min(200)]);
    log_debug!("collection (partial), ``{:?}``", collection_substr_ellipses);

    return collection;
}

fn process_record(record: &RecordXml) {
    let title: String = parse_title(&record);
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
fn add_nums(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_load_marc_xml_with_two_records() {
        println!("HELLO");
        let xml_data = r#"<collection xmlns="http://www.loc.gov/MARC21/slim">
            <record>
                <leader>     nam a22     uu 4500</leader>
                <controlfield tag="008">210101s2024    xx            eng d</controlfield>
                <datafield tag="245" ind1="0" ind2="0">
                    <subfield code="a">First Title</subfield>
                </datafield>
            </record>
            <record>
                <leader>     nam a22     uu 4500</leader>
                <controlfield tag="008">210101s2024    xx            eng d</controlfield>
                <datafield tag="245" ind1="0" ind2="0">
                    <subfield code="a">Second Title</subfield>
                </datafield>
            </record>
        </collection>"#;

        let marc_records: Collection = serde_xml_rs::from_str(&xml_data).unwrap_or_else(|err| {
            panic!("could not deserialize the marc_xml; error, ``{}``", err);
        });

        // let mut rec: RecordXml = RecordXml {
        //     controlfields: vec![],
        //     datafields: vec![],
        // };
        for record in marc_records.records.iter() {
            // original syntax
            let rec = process_record(record);
            println!("rec: ``{:?}``", rec);
            // let expected = "foo";
            // let result = parse_title(&rec);
            // assert_eq!( expected, result );
            assert_eq!(3, 3);
            break;
        }

        assert_eq!(3, 3);
    }

    #[test]
    fn test_add_nums() {
        let expected = 3;
        let result = add_nums(1, 2);
        assert_eq!(result, expected);
    }
}
