#!/usr/bin/env python3
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pyfzf.pyfzf import FzfPrompt
import argparse
import pprint
import re
# https://pythonhosted.org/PyDrive/oauth.html


class Google_Drive_Operation:
    def __init__(self):
        self.drive = self.signup()

    def signup(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        return drive

    def file_list(self):
        google_file_list = self.drive.ListFile().GetList()
        return google_file_list

    def create_file(self, file_name):
        extension = {
            "pdf": "application/pdf"
        }
        pattern = "\w.*\.(\w.*)"
        clip_extension = re.search(pattern, file_name).group(1)
        f = self.drive.CreateFile(
            {"title": file_name, "mimeType": extension[clip_extension]})
        # set local file
        f.SetContentFile(file_name)
        f.Upload()

    def remove_file(self):
        fzf = FzfPrompt()
        google_file_list = self.file_list()
        file_list = ["title:"+gf["title"]+" create_date:"+gf["createdDate"]
                     for gf in google_file_list]
        file_dict = {}
        for count, file_name in enumerate(file_list):
            file_dict[file_name] = count
        target_file = fzf.prompt(file_dict)[0]
        file_id = google_file_list[file_dict[target_file]]["id"]
        file1 = self.drive.CreateFile({'id': file_id})
        file1.Trash()  # Move file to trash.
        file1.Delete()  # Permanently delete the file.


def arg_parse():
    parser = argparse.ArgumentParser(
        description="operate google drive by program")
    parser.add_argument(
        "-f", "--f_list",  action="store_true", help="see file list")
    parser.add_argument(
        "-c", "--create", help="create file")
    parser.add_argument(
        "-r", "--remove", action="store_true", help="remove file")
    args = parser.parse_args()
    return args


def main():
    gd_operate = Google_Drive_Operation()
    args = arg_parse()

    if(args.f_list):
        google_file_list = gd_operate.file_list()
        file_list = ["title:"+gf["title"]+" create_date:"+gf["createdDate"]
                     for gf in google_file_list]
        pprint.pprint(file_list)

    elif(args.create):
        gd_operate.create_file(args.create)
    elif(args.remove):
        gd_operate.remove_file()


main()
