import scrapy
import csv
import re

# movielens links file (provides imdbIds for movielens movieIds)
links = "/media/felipe/SAMSUNG/movielens/ml-20m/links.csv"
imdb_synopsis_url_template = "http://www.imdb.com/title/tt{}/plotsummary"


class SynopsesSpider(scrapy.Spider):
    name = "synopses"
    clean_html_pat = r"<[^>]+>"

    def start_requests(self):

        ml_ids_and_imdb_ids = []

        with open(links, "r") as f:
            # skip header
            next(f)

            reader = csv.reader(f)

            for i, line in enumerate(reader):
                movieId, imdbId, _ = line
                ml_ids_and_imdb_ids.append((movieId, imdbId))

        urls = [imdb_synopsis_url_template.format(imdbId) for (_, imdbId) in ml_ids_and_imdb_ids]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        inner_text_with_html = response.css("li[id^=syn]").extract_first()

        if inner_text_with_html is None:
            synopsis = ''
        else:
            replaced_newlines = inner_text_with_html.replace("<br>", "\n")
            replaced_newlines = replaced_newlines.replace("\n\n", "\\\n\\\n")
            replaced_newlines = replaced_newlines.replace("\n", " ")

            clean_html = re.sub(self.clean_html_pat, "", replaced_newlines)
            synopsis = clean_html
            synopsis = synopsis.strip()

            if synopsis == "This plot synopsis is empty. Add a synopsis":
                synopsis = ''

        yield {'imdbId': self._extract_id(response.url), "synopsis": synopsis}

    def build_url(self, template, id):
        return template.format(id)

    def _extract_id(self, url):
        matches = re.search(r'(\d+)\/', url)

        if matches:
            return matches.group(1)
        else:
            return None
