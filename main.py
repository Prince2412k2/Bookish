from module import api_handler
from module.api_handler import main
from utils.logger_module import set_logger
from module.search import main as search


def print_book():
    search()


def test():
    set_logger()
    main()


if __name__ == "__main__":
    test()
