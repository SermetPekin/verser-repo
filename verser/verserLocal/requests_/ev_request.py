# ------------------------------------------------------------------------------
import requests as requests


from .my_cache import MyCache
from .my_cache import *
from .my_cache import load_pickle, save_pickle, save_pickle_helper
from .request_error_classes import REQUEST_ERROR_CODES

from ..utils.utils_general import *

from dataclasses import dataclass
from typing import Optional
from ..config.config import *


# ------------------------------------------------------------------------------

m_cache = MyCache()

# from evdspy.EVDSlocal.config.config import config
CANCEL_REQUEST_TEMP = False  # config.cancel_request_temp


def do_first_true_order(funcs, preds, url):
    conds = zip(funcs, preds)
    for func, pred in conds:
        if isinstance(pred, bool) and pred:
            v = func(url)
            return v
    return False


def mock_request(url, proxies=None) -> requests.models.Response:
    """ pytest will get this mock response object"""
    assert isinstance(url, str)
    file_name = str(Path(__file__).parent / "test_reg_result")
    assert Path(file_name + ".pickle").is_file(), f"file does not exist {file_name}"
    return load_pickle(file_name)


from ..config.config import *


def decide_request_for_test_real(url: str, proxies=None):
    """ Finally ready to make request """
    if config.current_mode_is_test:
        """ pytest will get this mock response object"""
        return mock_request(url, proxies)
    # print(f"WARNING : mock results are coming {url}")
    # return mock_request(url, proxies)

    if CANCEL_REQUEST_TEMP:
        print("request was cancelled...")
        return mock_request(url, proxies)
    if proxies is None:
        return requests.get(url)
    return requests.get(url, proxies=proxies)


@dataclass
class EVRequest:
    proxy: Optional[str] = False
    # args: Args = Args(sys.argv)
    last_url_checked: str = "NoneURL"

    # report : post init
    def __post_init__(self):
        self.URL_Instance = None

    def get_request_with_proxy(self, url: str, proxy: str):
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        return decide_request_for_test_real(url, proxies=proxies)

    def proxy_from_file(self, url: str):
        print("using proxy from file")
        return NotImplementedError
        # return self.get_request_with_proxy(url, self.args.proxy)

    def proxy_from_cmd_line(self, url: str):
        print("using proxy from commandline")
        return self.get_request_with_proxy(url, self.args.proxy)

    def check_if_request_ok(self, status_code: int):
        corrects = (200,)
        if status_code in corrects:
            # self.report.add(f"{status_code} returned. ")
            return True

        ExceptionClass = REQUEST_ERROR_CODES.get(status_code, None)
        if ExceptionClass:
            print(ExceptionClass)
            print(f"STATUS CODE : {status_code}\n url : {self.last_url_checked}")
            time.sleep(2)
            # raise ExceptionClass(self.__doc__)
        else:
            print(
                f"Program was checking request status code and noticed "
                f"{status_code} not included in  `REQUEST_ERROR_CODES`"
            )

        # self.report.add(f"{status_code} returned. ")
        return False

    def post_urls(self, url: str) -> tuple:

        # url = url.translate({ord(c): None for c in string.whitespace})
        url = URL_temizle(url)  # whitespace etc.

        self.last_url_checked = url

        return url

    def get_request_alternatives(self, url):
        result = do_first_true_order(
            funcs=[
                self.proxy_from_cmd_line,
                decide_request_for_test_real
            ],
            preds=[
                # self.args.proxy,
                False ,
                True],
            url=url
        )
        return result

    def check_result(self, result):
        if any(
                (
                        not hasattr(result, "status_code"),
                        not isinstance(result.status_code, int),
                        not self.check_if_request_ok(result.status_code)
                )
        ):
            print(f"request returned an error code {result.status_code} , url :  ")
            return False
        return True

    def get_request_before_cache(self, url: str):
        """
        decorated version of this function needs to be
        welcomed by this func to check api key etc.
        TODO
            stats for apikey and results
            warn user if there are many 500 status_code results for the certain api key
        """

        return self.get_request(url)

    def get_request(self, url: str):
        """
        first will check cache if there is cache
        below will not run at all
        """

        return self.get_request_by_checking_cache(url)

    @lru_cache_patched
    @m_cache.cache
    def get_request_by_checking_cache(self, url: str):
        """

        """

        return self.get_request_common(url)

    def get_request_by_checking_NO_CACHE(self, url: str):
        """

        """
        return self.get_request_common(url)

    def get_request_common(self, url: str):
        """
        first will check cache if there is cache
        below will not run at all
        """

        self.url = self.post_urls(url)
        if config.current_mode_is_test:
            print("Current Mode is test not requesting new data see initial.start_options")
            return load_test_pickle()
        """ if it is running we are definitely requesting """
        print("requesting!!")
        """ Exception checks will happen in function below"""
        result = self.get_request_alternatives(self.url)
        if not self.check_result(result):
            return False
        """ request looks solid we are ready to save """
        if result and self.check_if_request_ok(result.status_code):
            save_pickle_for_test(result)
        return result