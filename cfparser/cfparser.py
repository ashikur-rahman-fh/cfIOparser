"""
    This module container the parser classes and methods
    @author: Ashikur Rahman
"""
import requests
import threading
from bs4 import BeautifulSoup
from db.controller import get_setting_value
from logger import logger
from fshelper.fshelper import write_to_file


def get_page(url):
    """
        returns a html page fromt the given url
    """
    content = None
    try:
        response = requests.get(url, timeout=int(get_setting_value('HTTP_REQUEST_TIMEOUT')))

        if response.status_code != 200:
            raise Exception("HTTP request error while parsing {url}")

        content = response.content
    except Exception:
        pass

    return content

def parse_content_from_tag(soup, selector, one=False):
    """
        returns a beautiful soup from a soup
    """
    if one:
        return soup.select_one(selector)

    return soup.select(selector)

def parse_content_web(url, selector, one=False):
    """
        returns a beautiful soup object based on the selector from the web URL
    """
    soup = None
    try:
        soup = BeautifulSoup(markup=get_page(url), features="html.parser")
    except Exception:
        raise Exception("Invalid URL")
    if one:
        return soup.select_one(selector)

    return soup.select(selector)

class SELECTOR:
    """
        Selector class for select the html tag
    """
    BODY = 'body'
    PROBLEM_IDS = '.datatable .problems tr td:nth-child(1) a'
    PROBLEM_NAMES = '.datatable .problems tr td:nth-child(2) a'
    PROBLEM_INPUTS = '.sample-tests .input pre'
    PROBLEM_OUTPUTS = '.sample-tests .output pre'


class Problem:
    """
        Problem information
    """
    def __init__(self, key, name = "", info = "") -> None:
        self.key = key
        self.name = name
        self.info = info

    def set_name(self, name):
        self.name = name

    def set_info(self, info):
        self.info = info

    def __str__(self) -> str:
        return f"problem {self.key} - {self.name}"

    def __repr__(self) -> str:
        return f"problem {self.key} - {self.name}"

class CfScraper :
    """
        Scap the information from html page
    """

    base_url = "https://codeforces.com/"
    def __init__(self, contest_id) -> None:
        self.contest_id = contest_id
        self.contest_page_body = None
        self.problems = []

    def get_contest_url(self):
        """
            Generate the contest url
        """
        return f"{self.base_url}" + f"contest/{self.contest_id}/"

    def get_problem_url(self, problem):
        """
            Generate the problem url
        """
        return self.get_contest_url() + f"problem/{problem}/"

    def set_contest_page_body(self):
        """
            Download the page
        """
        contest_url = self.get_contest_url()
        try:
            logger.info(f"Contest {self.contest_id} parsing started")
            self.contest_page_body = parse_content_web(contest_url, SELECTOR.BODY, one=True)
            logger.success(f"Contest {self.contest_id} - Contest page parsed")
        except Exception:
            logger.fetal(f"Can not parse the main contest page - {contest_url}")

    def scap_home_page(self):
        """
            Scap the homepage
        """
        self.set_contest_page_body()
        problem_ids_tag = parse_content_from_tag(self.contest_page_body, SELECTOR.PROBLEM_IDS)
        problem_names_tag = parse_content_from_tag(self.contest_page_body, SELECTOR.PROBLEM_NAMES)

        for p_id, p_name in zip(problem_ids_tag, problem_names_tag):
            self.problems.append(Problem(
                self.normalize_text(p_id.get_text()),
                self.normalize_text(p_name.get_text())
            ))

    def scrap_problem_page(self, key):
        """
            Scrap indevidual problem
        """
        problem_url = self.get_problem_url(key)
        logger.info(f'Parsing problem {key}')
        problem_body = ""
        try:
            problem_body = parse_content_web(problem_url, 'body', one=True)
        except Exception:
            logger.error(f'Parsing failed problem {key}')
            return

        def get_samples(selector, stype):
            """Getting input from problem"""
            samples = parse_content_from_tag(problem_body, selector=selector)

            def get_info_with_new_format(tags):
                ret = ""
                for div in tags:
                    ret += self.normalize_text(div.get_text()) + "\n"

                return ret

            def get_info_with_old_format(tag):
                return self.normalize_text(tag.get_text()) + "\n"

            for index, sample in enumerate(samples):
                # handle each input separately
                all_divs = sample.find_all('div')

                sample_text = ""
                if all_divs:
                    sample_text = get_info_with_new_format(all_divs)
                else:
                    sample_text = get_info_with_old_format(sample)

                # generate file path
                pref = 'in' if stype  == 'input' else 'out'
                file_name = f'cf-{self.contest_id}/{key}/{stype}/{pref}{index}'.lower()
                write_to_file(file_name=file_name, value=sample_text)


        get_samples(SELECTOR.PROBLEM_INPUTS, 'input')
        get_samples(SELECTOR.PROBLEM_OUTPUTS, 'output')
        logger.success(f'Parsed problem {key}')

    def normalize_text(self, text):
        """
            Clean up the text
        """
        return str(text).strip(' \t\r\n')

    def display_stats(self):
        """
            display contest stats
        """
        stat_text = \
f"""

Number of problems: {len(self.problems)}
Happy Coding!

"""
        print(stat_text)

    def run(self):
        """
            Main driver function
        """
        self.scap_home_page()
        p_scrapers = []
        for problem in self.problems:
            p_thread = threading.Thread(target=self.scrap_problem_page, args=[problem.key])
            p_scrapers.append(p_thread)

        for scapper in p_scrapers:
            scapper.start()

        for scapper in p_scrapers:
            scapper.join()

def parse_contest(contest_id):
    """Contest scrapper API"""
    cf_scraper = CfScraper(contest_id=contest_id)
    cf_scraper.run()
    cf_scraper.display_stats()
