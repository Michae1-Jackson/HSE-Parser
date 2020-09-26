import requests
import os

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/84.0.4147.105 Safari/537.36', 'accept': '*/*'}


def slash_handler(name):
    return ' aka '.join([half.strip() for half in name.split('/')])


# For debug
def print_dict(d: dict):
    for k, v in d.items():
        print(f'{k}: {v}')


def print_degree(degree: dict):
    for program, prog_tutors in degree.items():
        print(f'{program}\n')
        for tutor in prog_tutors:
            tutor.description()


# Request handler returning html text or empty string
def get_html_text(url):
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f'ALARM SOMETHING WRONG\nSTATUS CODE: {response.status_code}')
        return ''


# Tutor class
# Designed to make it easier to get more information in the future when needed
class Tutor:
    def __init__(self, name=None, link=None, img_url=None, img_path=None, position=None, subjects=None):
        subjects: list
        self.name = name
        self.link = link
        self.img_url = img_url
        self.img_path = img_path
        self.position = position
        self.subjects = subjects

    def description(self):
        return f'Name: {self.name}\n' \
               f'Profile: {self.link}\n' \
               f'Image url: {self.img_url}\n' \
               f'Image path: {self.img_path}\n' \
               f'Position: {self.position}\n' \
               f'Subjects: {self.subjects}\n'

    def csv_entry(self):
        return [self.name, self.link, self.img_url,
                self.img_path, self.position, self.subjects]

    def get_image(self, img_url=None, img_path=None):
        if not img_url:
            img_url = self.img_url
        if not img_path:
            img_path = self.img_path
        if not os.path.exists(img_path): os.makedirs(img_path)
        path = f'{img_path}{self.name}.png'
        if not os.path.exists(path):
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(path, 'wb') as img:
                    img.write(response.content)
                print(f'Image from {img_url} was added to {img_path}')
            else:
                print('Can`t download image\n'
                      f'Status code: {response.status_code}')
        else:
            print('Image alredy exist')
