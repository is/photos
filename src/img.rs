#![allow(dead_code)]

use std::any::Any;
use lazy_static::lazy_static;
use regex::Regex;
use sha2::Digest;
use std::path::Path;
use std::string::String;
use exif::{In, Tag, Value};

pub struct MetaCore {
    pub model: String,
    pub datetime: String,
    pub number: String,
    pub ext: String,
}

pub enum FileMeta {
    V1(MetaCore),
    V2(MetaCore),
}

fn split_path_2(path: &str) -> Option<(&str, &str, &str)> {
    let path = Path::new(path);
    Some((
        path.parent()?.as_os_str().to_str()?,
        path.file_stem()?.to_str()?,
        path.extension()?.to_str()?,
    ))
}

fn number_from_file_name_hash(file_name: &str) -> String {
    let mut hasher = sha2::Sha256::new();
    hasher.update(file_name);

    let digest = hasher.finalize();
    let tail = &digest[digest.len() - 4..];
    format!(
        "{:05}",
        u32::from_be_bytes(TryInto::<[u8; 4]>::try_into(tail).unwrap()) % MAX_NUMBER
    )
}

fn number_from_file_name(file_name: &str) -> String {
    if file_name.len() <= 9 {
        if let Some(captures) = NUMBER_IN_FILE_NAME.captures(file_name) {
            let number = captures.get(1).unwrap().as_str();
            let number = format!("{:05}", number.parse::<u32>().unwrap() % MAX_NUMBER);
            return number;
        }
    }
    number_from_file_name_hash(file_name)
}

const MAX_NUMBER: u32 = 100000;

lazy_static! {
    static ref FILE_NAME_PATTERN_V1: Regex = Regex::new(r"(\D)_(\d{5})__(\d{8}_\d{6})").unwrap();
    static ref FILE_NAME_PATTERN_V2: Regex =
        Regex::new(r"(\d{8}_\d{6})__(\d{2,5})_(.{1,})").unwrap();
    static ref NUMBER_IN_FILE_NAME: Regex = Regex::new(r".+?(\d+)").unwrap();
}

impl FileMeta {
    pub fn from_path(path: &str) -> Option<FileMeta> {
        let (_dir, file_stem, file_ext) = split_path_2(path)?;

        if let Some(captures) = FILE_NAME_PATTERN_V1.captures(file_stem) {
            return Some(FileMeta::V1(MetaCore {
                model: captures.get(1)?.as_str().to_string(),
                datetime: captures.get(3)?.as_str().to_string(),
                number: captures.get(2)?.as_str().to_string(),
                ext: file_ext.to_uppercase(),
            }));
        }

        if let Some(captures) = FILE_NAME_PATTERN_V2.captures(file_stem) {
            return Some(FileMeta::V2(MetaCore {
                model: captures.get(3)?.as_str().to_string(),
                datetime: captures.get(1)?.as_str().to_string(),
                number: captures.get(2)?.as_str().to_string(),
                ext: file_ext.to_uppercase(),
            }));
        }
        None
    }

    #[allow(unused)]
    pub fn from_exif(path: &str) -> Option<FileMeta> {
        let (dir, file_stem, file_ext) = split_path_2(path)?;
        let number = number_from_file_name(file_stem);

        let file = std::fs::File::open(path).ok()?;
        let mut buf_reader = std::io::BufReader::new(&file);
        let exif_reader = exif::Reader::new();
        let exif = exif_reader.read_from_container(&mut buf_reader).ok()?;

        let model_field = exif.get_field(Tag::Model, In::PRIMARY);
        let create_date_field = exif.get_field(Tag::DateTimeOriginal, In::PRIMARY);

        if model_field.is_none() || create_date_field.is_none() {
            return None;
        };
        None
    }
}

#[cfg(test)]
mod tests {
    use crate::img::{number_from_file_name, FileMeta};
    use regex::Regex;
    use sha2::Digest;
    use std::ffi::OsStr;
    use std::path::{Path, PathBuf};

    static FILE_NAME_1: &str = "A_02104__20230105_150108.arw";
    static FILE_NAME_2: &str = "20230105_150108__03212_A7R4.arw";

    #[test]
    fn test_number_in_name() {
        assert_eq!(number_from_file_name("DSC03212"), "03212");
        assert_eq!(
            number_from_file_name("BB40B3F3-2D88-4023-82BA-90CAE2C4DB45"),
            "36957"
        );
    }

    #[test]
    fn test_hash_sha2() {
        let mut hasher = sha2::Sha256::new();
        hasher.update(b"hello world");
        let digest = hasher.finalize();
        let tail = &digest[(digest.len() - 4)..];
        let sign = u32::from_be_bytes(TryInto::<[u8; 4]>::try_into(tail).unwrap());
        assert_eq!(sign, 3807366633);
        assert_eq!(format!("{:05}", sign % 10000), "06633");
        /*
        assert_eq!(digest[..], hex!("b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9")[..]);
        */
    }

    #[test]
    fn test_path_buf() {
        let path_buf = PathBuf::from("/home/admin/.config");

        assert_eq!(
            "/home/admin",
            path_buf.parent().and_then(Path::to_str).unwrap()
        );
        assert_eq!(
            ".config",
            path_buf.file_name().and_then(OsStr::to_str).unwrap()
        );

        let path_buf = PathBuf::from("HELLO.ME.WORLD");
        assert!(path_buf.parent().and_then(Path::to_str).unwrap().is_empty());
        assert_eq!(
            "WORLD",
            path_buf.as_path().extension().unwrap().to_str().unwrap()
        );
        assert_eq!(
            "HELLO.ME",
            path_buf.as_path().file_stem().unwrap().to_str().unwrap()
        );
    }

    #[test]
    fn test_split_path() {
        let (p0, p1, p2) = super::split_path_2("A_02104__20230105_150108.ARW").unwrap();
        assert_eq!("", p0);
        assert_eq!("A_02104__20230105_150108", p1);
        assert_eq!("ARW", p2);

        let (p0, p1, p2) = super::split_path_2("ABC/A_02104__20230105_150108.ARW").unwrap();
        assert_eq!("ABC", p0);
        assert_eq!("A_02104__20230105_150108", p1);
        assert_eq!("ARW", p2);
    }

    #[test]
    fn test_regex_0() {
        let name = "A_02104__20230105_150108";
        let r0 = Regex::new(r"(\D)_(\d{5})__(\d{8}_\d{6})").unwrap();
        let captures = r0.captures(name).unwrap();
        assert_eq!(
            "A_02104__20230105_150108",
            captures.get(0).unwrap().as_str()
        );
        assert_eq!("A", captures.get(1).unwrap().as_str());
        assert_eq!("02104", captures.get(2).unwrap().as_str());
        assert_eq!("20230105_150108", captures.get(3).unwrap().as_str());
    }
}