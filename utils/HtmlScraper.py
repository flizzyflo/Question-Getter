from typing import Tuple

import requests
from bs4 import ResultSet, BeautifulSoup


def get_relevant_html(current_response: requests.Response = None) -> Tuple[ResultSet, ResultSet]:
    """
    Wrapper function to encapsulate the beautiful soup logic which extracts the relevant html information for the
    later processing of the data.

    Returns:
        tuple[ResultSet]: Returning a tuple of bs4.Result sets. First element in tuple is the selection div result set,
        which contains all the question related information. Second element are the correct answers for the respective question.
    """

    soup: BeautifulSoup = BeautifulSoup(current_response.content, 'html.parser')
    selection_divs: ResultSet = soup.find_all("div", {"class": "formulation clearfix" })
    correct_answer_divs: ResultSet = soup.find_all("div", {"class": "rightanswer"})

    return selection_divs, correct_answer_divs
