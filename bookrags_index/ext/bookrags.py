import re
import requests
from ..ext.definitions import Urls, ProductType
from ..ext.product import Product
from ..ext.lens import Lens
from ..ext.helper import resolve_type


class BookRags:
    """
    Interface class for communicating with the API
    """

    def __init__(self, username: str, password: str) -> None:
        """
        Creates a session given login details
        """
        self.__details = {
            'edEmailOrName': username,
            'edPW': password
        }
        self._session = requests.Session()
        self._setup_cookies()
        self._login()

    def _setup_cookies(self) -> None:
        """
        Not required
        """
        self._session.cookies['layout'] = 'desktop'
        self._session.get(Urls.WEBSITE_URL)
        self._session.get(Urls.SESSION_URL)

    def _login(self) -> None:
        """
        Authenticates the current session using the given details
        """
        self._session.post(
            Urls.LOGIN_URL,
            data=self.__details)

    def is_logged_in(self) -> bool:
        """
        Checks if the current session is signed in
        """
        check = self._session.get(
            Urls.ACCOUNT_URL,
            allow_redirects=False).text

        return len(check) > 0

    def get_session(self) -> requests.session:
        return self._session

    def logout(self) -> None:
        """
        Signs out of the user account from the active session
        """
        self._session.get(Urls.LOGOUT_URL)

    def resolve_product(self, link: str) -> Product:
        """
        Given a link, it will resolve into the product page
        """
        type = resolve_type(self._session, link)

        if type == ProductType.UNKNOWN or \
                type == ProductType.LESSON_PLAN or \
                type == ProductType.LENS:
            return None

        return Product(self._session, link, type)

    def resolve_study_plan(self, link: str) -> Lens:
        """
        Given a link, it will resolve it into the study guide page and return a Lens instance
        """
        type = resolve_type(self._session, link)

        if type == ProductType.UNKNOWN:
            return None

        if type == ProductType.LENS:
            return Lens(self._session, link)

        page = self._session.get(link).text

        study_guide = re.search("href=\'(.*?)\'", re.search(
            '<div id=\'contentSPUpsellBlock\'>(.*?)</div>', page, flags=re.DOTALL
        ).group()).group(1)

        return Lens(self._session, study_guide)

    def search(self, query: str):
        """
        Perform a search query and return the results
        """
        pass