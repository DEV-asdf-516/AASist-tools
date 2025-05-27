from tkinter import filedialog

from guidance.aasx_file_reader import AasxFileReader
from guidance.submodel_table_extractor import TableFormat
from guidance.xml.xml_table_extractor import XmlTableExtractor
from guidance.xml.xml_table_parser import XmlTableParser
from gui.aasist_guidance.main import main as guidance_main


def main():
    guidance_main()


if __name__ == "__main__":
    main()
