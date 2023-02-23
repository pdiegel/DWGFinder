import os
import time


class DWGFiles:
    file_number_length = 8

    def __init__(self, file_number) -> None:
        # file_number = dpg.get_value('file_number')
        self.file_number = file_number
        if not self.verify_file_number():
            return
        self.year = self.file_number[:2]
        self.month = self.get_month()
        self.short_file_number = self.get_short_file_number()
        self.file_path = self.get_file_path()
        self.file_list = self.get_file_list()
        self.file_dict = self.get_file_dict()
        self.formatted_file_list = self.get_formatted_file_list()
        self.newest_file = self.get_newest_file()

    def verify_file_number(self):
        if len(self.file_number) == DWGFiles.file_number_length:
            return True
        else:
            raise ValueError('Invalid Job Number')

    def get_month(self):
        month = self.file_number[2:4]
        if int(self.year) > 89:
            if int(month) < 10:
                month = self.file_number[3]
        return month

    def get_short_file_number(self):
        short_file_number = f'{self.year}{self.month}{self.file_number[5:8]}'
        return short_file_number

    def get_file_path(self):
        file_path = f'//server/dwg/{self.year}dwg/{self.month}/'
        return file_path

    def get_file_name(self, file_path):
        file_name = ''
        if '/' in file_path:
            file_name = file_path.split('/')[-1]
            if '\\' in file_name:
                file_name = file_name.split('\\')[-1]
        return file_name

    def get_file_list(self):
        file_list = []
        for (dir, _, files) in os.walk(self.file_path, topdown=True):
            for file in files:
                current_file_path = os.path.join(dir, file)
                is_dwg_file = file.lower().endswith('.dwg')
                if not is_dwg_file:
                    continue
                if file.startswith(self.file_number):
                    file_list.append(current_file_path)
                elif file.startswith(self.short_file_number):
                    file_list.append(current_file_path)

        if file_list:
            return file_list

    def get_file_dict(self):
        file_list = self.get_file_list()
        file_dict = {}
        for file in file_list:
            file_date = self.format_date(file)
            file_dict[file] = file_date
        return file_dict

    def get_formatted_file_list(self):
        formatted_file_list = []
        for item in self.file_list:
            file_name = self.get_file_name(item)
            formatted_file_list.append(f'{file_name} | {self.file_dict[item]}')
        return formatted_file_list

    def get_specific_file_path(self, file_name):
        for file in self.file_list:
            if file_name in file:
                if '\\' in file:
                    return "/".join(file.split('\\')[:-1])
                return "/".join(file.split('/')[:-1])

    def get_newest_file(self):
        newest_creation_time = 0
        newest_file = ''
        for file in self.file_list:
            file_creation_time = os.path.getctime(file)
            if file_creation_time > newest_creation_time:
                newest_creation_time = file_creation_time
                newest_file = file

        return newest_file

    def format_date(self, file):
        file_ctime = os.path.getctime(os.path.join(self.file_path, file))
        file_date = time.ctime(file_ctime)
        file_date_list = file_date.split(' ')
        formatted_file_date = f'{file_date_list[1]} {file_date_list[2]}, \
{file_date_list[4]}'
        return formatted_file_date
