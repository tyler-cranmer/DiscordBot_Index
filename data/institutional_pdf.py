import os
import discord
import fileinput
from git import Repo
import datetime
import time
import json

# Opens Json File to check for Admin Id
with open("./config.json") as f:
    configData = json.load(f)

path = configData['Path']
html_path = configData['html_path']
path2 = configData['script_path']


class Automate:
    def __init__(self):
        working = '/Users/tylercranmer/Dev/indexcoop.github.io'
        repo = Repo(working)
        assert not repo.bare

        #repo.git.checkout('-b', 'testing_automate')

    def update_html(file_name, year, month):
        pdf_name = file_name
        working = path
        repo = Repo(working)
        assert not repo.bare
        index_html = html_path


        if pdf_name[:3] == 'mvi':    
            html_line = f'           <a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/{year}/{month}/{pdf_name}" target="_blank" class="link-9">Learn More</a><br>'
            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                for line in f:
                    if 'link-9' in line:
                        print(html_line, end = '\n')
                    else:
                        print(line, end='')  

        elif pdf_name[:3] == 'dpi':    
            html_line = f'           <a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/{year}/{month}/{pdf_name}" target="_blank" class="link-10">Learn More</a><br>'
            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                for line in f:
                    if 'link-10' in line:
                        print(html_line, end = '\n')
                    else:
                        print(line, end='')  

        elif pdf_name[:3] == 'fli':    
            html_line = f'           <a href="https://raw.githubusercontent.com/IndexCoop/indexcoop.github.io/master/assets/{year}/{month}/{pdf_name}" target="_blank" class="link-11">Learn <span>More</span></a>'
            with fileinput.FileInput(index_html, inplace = True, backup ='.bak') as f:
                for line in f:
                    if 'link-11' in line:
                        print(html_line, end = '\n')
                    else:
                        print(line, end='')  

            # time.sleep(1)
            # repo.git.add(all=True)
            # time.sleep(1)
            # repo.git.commit('-m', f'{file_name} has been added into repo by hooty bot')
        return
        