import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.pagina12.com.ar/'

XPATH_LINK_TO_ARTICLE = '//div[@class="article-title"]/a/@href'
XPATH_TITLE = '//article[@class="article-full section"]//h1[not(@class)]/text()'
XPATH_SUMMARY = '//article[@class="article-full section"]//h3[not(@class)]/text()'
XPATH_BODY = '//div[@class="article-main-content article-text  "]//p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed_notice = html.fromstring(notice)
            try:
                title = parsed_notice.xpath(XPATH_TITLE)[0]
                # title = title.replace('\"', '')
    o no sólo reconocerlo, si no trabajar en ello, para que cada persona pueda elegir el/los beneficios qué mas se ajusten a su parecer 😊.
El Cronista Comercial
El Cronista Comercial 31.975 seguidores 2 días •
hace 2 días
Cada vez más empresas apelan al "salario emocional" para para atraer y retener talento. Se trata de aquellas retribuciones fuera de le económico que un trabajador puede conseguir por su trabajo.

Conocé más de este concepto 👇
            body = parsed_notice.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            # parsed es el contenido de home listo para scrapear
            parsed = html.fromstring(home)
            link_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in link_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

    return print('Done!')


def run():
    parse_home()


if __name__ == '__main__':
    run()