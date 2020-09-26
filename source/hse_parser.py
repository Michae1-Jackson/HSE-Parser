from bs4 import BeautifulSoup
from utils import get_html_text, Tutor, slash_handler
# print_degree
from time import sleep

# Get a list of programs
def get_edu_programs(html):
    # Lists of names and urls
    spb_bac_names_list = []
    spb_bac_urls_list = []
    spb_mag_names_list = []
    spb_mag_urls_list = []

    # Get html describing programs
    soup = BeautifulSoup(html, 'html.parser')
    clear_edu_progs = ''.join(map(str, soup.find_all('div', class_=['b-row edu-programm__item'])))
    # Get list of programs names and links
    soup = BeautifulSoup(clear_edu_progs, 'html.parser')
    list_of_url_tags = soup.find_all('a', class_='link')
    for url_tag in list_of_url_tags:
        url = url_tag['href']
        if url.startswith('https://spb.hse.ru/ba'):
            spb_bac_names_list.append(url_tag.get_text())
            spb_bac_urls_list.append(url)
        elif url.startswith('https://spb.hse.ru/ma'):
            spb_mag_names_list.append(url_tag.get_text())
            spb_mag_urls_list.append(url)

    return spb_bac_names_list, spb_bac_urls_list, \
        spb_mag_names_list, spb_mag_urls_list


# Get html programs to speed up future parsing if needed
def get_html_tutors(names, urls):
    html_dict = {}
    urls_dict = dict(zip(names, urls))
    for name, url in urls_dict.items():
        url = f'{url}tutors/?year=2020'
        html = get_html_text(url)
        if '/' in name: name = slash_handler(name)
        html_dict[name] = html
        print('.', end='')
        sleep(.2)
    return html_dict


# Get tutors from html
def get_tutors(prog_name, html, degree='Other'):
    prog_tutors = []
    soup = BeautifulSoup(html, 'html.parser')
    tutor_block_list = list(map(str, soup.find_all('div', class_=['b-greetings__item b-greetings__tutor'])))
    for tutor_block in tutor_block_list:
        tutor = Tutor()
        block = BeautifulSoup(tutor_block, 'html.parser')
        # Get name
        tutor.name = block.find(['a', 'ins'], class_='b').get_text().strip()
        # Get link on profile
        link = block.find('a', class_='b')
        if link: tutor.link = f"https://hse.ru{link['href'].strip()}"
        # Get url of image and path where to save
        img_url_tag = block.find('img', class_=['lazy', '__iwc'])
        tutor.img_url = f"https://hse.ru{img_url_tag['data-src'].strip()}"
        tutor.img_path = f'docs/Programs/{degree}/Tutors/{prog_name}/photos/'
        # Get position
        position = block.find('div', style='margin-top: 1em;')
        if position.get_text():
            tutor.position = position.get_text().strip()
        # Get subjects
        sub_tags = block.find_all('div', class_='with-indent1')
        if sub_tags:
            tutor.subjects = [sub_tag.get_text() for sub_tag in sub_tags]
        prog_tutors.append(tutor)
        # tutor.description()
    return prog_tutors

# Transform html pages to tutors dictionary
def degree_folder_to_tutors_dict(degree):
    tutors_dict = {}
    path = f'docs/{degree}_links.txt'
    with open(path, 'r', encoding='utf-8') \
            as named_links:  # name: link
        for line in named_links:
            prog_name, link = line.strip().split(': ')
            if '/' in prog_name: prog_name = slash_handler(prog_name)
            path = f'docs/Tutors_html/{degree}/{prog_name}.html'
            with open(path, 'r', encoding='utf-8') as page:
                tutors_html = page.read()
                program = f'{prog_name}\n{link}'
                tutors_dict[program] = get_tutors(prog_name, tutors_html, degree)
    return tutors_dict


# def parse(url):
def parse():
    # Primary parsing
    """ html = get_html_text(url)
    bac_names_list, bac_urls_list, \
    mag_names_list, mag_urls_list = get_edu_programs(html)
    bac_html_dict = get_html_tutors(bac_names_list, bac_urls_list)
    mag_html_dict = get_html_tutors(mag_names_list, mag_urls_list)"""
    tutors_bac = degree_folder_to_tutors_dict('Undergraduate')
    # print_degree(tutors_bac)
    tutors_mag = degree_folder_to_tutors_dict('Magistracy')
    # print_degree(tutors_mag)

    return tutors_bac, tutors_mag
