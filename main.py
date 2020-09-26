# python ver. 3.8.5
# encoding utf-8
from source.hse_parser import parse
from source.saver import save_as_csv
# from source.saver import save_as_txt_or_html, save_as_doc

URL = 'https://spb.hse.ru/education/'


def main():
    # parse(URL)
    tutors_bac, tutors_mag = parse()
    # tutors_bac['Востоковедение\nhttps://spb.hse.ru/ba/oriental/'][0].description()
    # tutors_bac['Востоковедение\nhttps://spb.hse.ru/ba/oriental/'][0].get_image()

    # Save to CSV format
    for program, tutors in tutors_bac.items():
        prog_name = program.split('\n')[0]
        path = f'docs/Programs/Undergraduate/Tutors/{prog_name}/'
        save_as_csv(content=tutors,
                    path=path,
                    file_name=f'{prog_name}.csv')
    for program, tutors in tutors_mag.items():
        prog_name = program.split('\n')[0]
        path = f'docs/Programs/Magistracy/Tutors/{prog_name}/'
        save_as_csv(content=tutors,
                    path=path,
                    file_name=f'{prog_name}.csv')

    # Save to Docx format
    """
    for program, tutors in tutors_bac.items():
        prog_name, prog_link = program.split('\n')
        content = [prog_name, prog_link, tutors]
        path = f'docs/Programs/Undergraduate/Tutors/{prog_name}/'
        save_as_doc(content=content,
                    path=path,
                    file_name=f'{prog_name}.docx')
    for program, tutors in tutors_mag.items():
        prog_name, prog_link = program.split('\n')
        content = [prog_name, prog_link, tutors]
        path = f'docs/Programs/Magistracy/Tutors/{prog_name}/'
        save_as_doc(content=content,
                    path=path,
                    file_name=f'{prog_name}.docx')"""

# html pages was saved in very similar way
    """
    for name, link in bac.items():
        content = f'{name}: {link}\n'
        save_as_txt_or_html(content=content,
                            path='docs/Tutors_html/',
                            file_name=f'Undergraduate_links.txt',
                            add=True)
    for name, link in mag.items():
        content = f'{name}: {link}\n'
        save_as_txt_or_html(content=content,
                            path='docs/Tutors_html/',
                            file_name=f'Magistracy_links.txt',
                            add=True)"""

if __name__ == '__main__':
    main()
