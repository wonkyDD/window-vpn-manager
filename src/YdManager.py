"""
https://velog.io/@sangyeon217/deprecation-warning-executablepath-has-been-deprecated
https://choihyuunmin.tistory.com/82

TODO : 병렬 처리  
import aiohttp, asyncio

from concurrent import futures
from threading import Thread
from multiprocessing import Process, Queue
from multiprocessing.dummy import Pool

"""

import logging

# from logging.handlers import RotatingFileHandler
import os
import sqlite3
from time import sleep, time
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from .database import get_database
from .settings import (
    DB_TABLE_NAMES,
    DRIVER_TYPES,
    LOG_NAME,
    LOG_PATH,
    SCREENSHOT_NAMES,
    SCREENSHOT_PATH,
    TARGET_LINKS,
    TXT_NAME,
    TXT_PATH,
)
from .util import dash_to_underscore, timer
from .xpath_compile import read_xpath


class YdManager:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        driver_type: Optional[str] = DRIVER_TYPES.get("firefox"),
        headless: bool = True,
        show_logs: bool = True,
        show_db: bool = True,
        show_elapsed: bool = True,
    ) -> None:

        # driver
        self.headless = headless
        self._driver_type = driver_type
        self._driver = self.init_driver(self.driver_type)

        # debug
        self.show_logs = show_logs
        self.show_db = show_db
        self.show_elapsed = show_elapsed
        if self.show_elapsed:
            self.start_time = time()

        # TODO : 이거 에러남
        # self.logger = self.init_logger(self.show_logs)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def driver(self):
        return self._driver

    @property
    def driver_type(self):
        return self._driver_type

    def set_chrome_driver(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
        return driver

    def set_firefox_driver(self) -> webdriver.Firefox:
        firefox_options = webdriver.FirefoxOptions()
        if self.headless:
            firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=firefox_options
        )

        return driver

    def init_driver(self, driver_type: str) -> webdriver.Firefox | webdriver.Chrome:
        self._driver_type = driver_type

        if driver_type == "Firefox":
            driver = self.set_firefox_driver()

        elif driver_type == "Chrome":
            driver = self.set_chrome_driver()  # type: ignore

        return driver

    def exit_driver(self) -> float:
        self._driver.close()
        self._driver.quit()

        if self.show_elapsed:
            elapsed_time = time() - self.start_time
            return timer(elapsed_time)

        # TODO :
        # 더 좋은 방식이 없을까?
        return -1

    def get(self, link: Optional[str]):
        if not link:
            return
        self._driver.get(link)

    # TODO :
    # XPATH로 수정
    def get_all_videolinks(self) -> List[Tuple[str, str]]:
        elements = self._driver.find_elements(By.TAG_NAME, "a")
        titles_and_links = []

        for e in elements:
            href = e.get_attribute("href")
            parsed = urlparse(href)
            path = parsed.path

            s = []
            if isinstance(path, str):
                s = path.split("/")

            if len(s) > 1 and s[1].isdigit() and len(e.text) > 0:
                title = e.get_attribute("title")
                pair = (title, href)
                titles_and_links.append(pair)

        return titles_and_links

    # TODO :
    # DEBUG용
    def get_all_first_videoids(self) -> Dict[str, str]:
        new_datas: Dict[str, str] = {}
        for genre, link in TARGET_LINKS.items():
            self._driver.get(link)

            first_link = self.get_first_videolink()
            new_id = self.parse_videoid(first_link[1])
            new_datas.update({genre: str(new_id)})

        return new_datas

    def get_first_videolink(self) -> Tuple:
        elememts = self._driver.find_elements(By.TAG_NAME, "a")

        for e in elememts:
            href = e.get_attribute("href")
            parsed = urlparse(href)
            path = parsed.path

            s = []
            if isinstance(path, str):
                s = path.split("/")

            if len(s) > 1 and s[1].isdigit():
                title = e.get_attribute("title")
                break

        return (title, href)

    # TODO:
    # 1. link에 대한 validate없이 제대로된 link만 넣어주는 상황을 가정해도 될까?
    # 2. int로 return하는 게 맞을까?
    def parse_videoid(self, link: str) -> str:
        parsed = urlparse(link)
        path = parsed.path
        s = path.split("/")

        return s[1]

    # TODO :
    # WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@class='lazy']")))
    def screenshot_fullpage(
        self, screenshot_path: str, screenshot_name: str, sleep_time: float = 2
    ):
        original_size = self._driver.get_window_size()
        scroll_width = self._driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        scroll_height = self._driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )

        self._driver.set_window_size(scroll_width, scroll_height)
        sleep(sleep_time)
        self._driver.find_element(By.TAG_NAME, "body").screenshot(
            f"{screenshot_path}{screenshot_name}"
        )
        self._driver.set_window_size(original_size["width"], original_size["height"])

    def screenshot_element(
        self,
        by: str,
        identifier: str,
        screenshot_path: str,
        screenshot_name: Optional[str],
        sleep_time: float = 2,
    ):
        sleep(sleep_time)

        if by.lower() == "xpath":
            self._driver.find_element(By.XPATH, identifier).screenshot(
                f"{screenshot_path}{screenshot_name}"
            )
        elif by.lower() == "id":
            self._driver.find_element(By.ID, identifier).screenshot(
                f"{screenshot_path}{screenshot_name}"
            )
        elif by.lower() == "tag_name":
            self._driver.find_element(By.TAG_NAME, identifier).screenshot(
                f"{screenshot_path}{screenshot_name}"
            )
        elif by.lower() == "class_name":
            self._driver.find_element(By.CLASS_NAME, identifier).screenshot(
                f"{screenshot_path}{screenshot_name}"
            )
        elif by.lower() == "name":
            self._driver.find_element(By.NAME, identifier).screenshot(
                f"{screenshot_path}{screenshot_name}"
            )
        else:
            # TODO :
            # error logging 시스템으로 로그출력 ?
            pass

    # TODO :
    # DEBUG용
    def get_all_videogrid_screenshots(self, sleep_time: float = 2):
        screenshots = os.listdir(SCREENSHOT_PATH)
        for s in screenshots:
            if os.path.isfile(SCREENSHOT_PATH + s):
                os.remove(SCREENSHOT_PATH + s)

        for key in TARGET_LINKS.keys():
            self.get(TARGET_LINKS.get(key))
            sleep(sleep_time)
            self.screenshot_element(
                By.XPATH,
                read_xpath("video", "video_grid"),
                SCREENSHOT_PATH,
                SCREENSHOT_NAMES.get(key),
            )

    def store_videoid_to_txt(self, new_datas: Dict[str, str]):
        result = []
        with open(TXT_PATH + TXT_NAME, "w", encoding="utf-8") as f:
            for genre, videoid in new_datas.items():
                d = f"{genre}: {videoid}\n"
                result.append(d)

            f.writelines(result)

    def store_videoid_to_sqlite(self, new_datas: Dict[str, str]):
        db_address = get_database()

        try:
            # self.backup_db()
            db = sqlite3.connect(db_address)

            with db:
                db.row_factory = sqlite3.Row
                cur = db.cursor()
                videoid_table_name = [
                    name for name in DB_TABLE_NAMES if name == "videoId"
                ][0]

                INSERT_INTO_VIDEOID = f"""
                    INSERT INTO {videoid_table_name} 
                    (korean_porn, korean_bj, asian_porn_movies, china_porn)
                    VALUES(:korean_porn, :korean_bj, :asian_porn_movies, :china_porn)"""

                cur.execute(INSERT_INTO_VIDEOID, new_datas)
                db.commit()

                if self.show_db:
                    cur.execute("SELECT * FROM videoId")
                    rows = cur.fetchall()

                    for row in rows:
                        print(row["id"], row["korean_porn"])

        except Exception as exc:
            # TODO : logger로 교체
            print(str(exc).encode("utf-8"))

        finally:
            if db:
                db.close()

    def renew_videoid_table(self):
        new_datas = {}
        for genre, target_link in TARGET_LINKS.items():
            self.get(target_link)
            link = self.get_first_videolink()[1]
            new_videoid = self.parse_videoid(link)

            new_datas.update({genre: new_videoid})
            self.screenshot_element(
                "xpath",
                read_xpath("video", "video_grid"),
                SCREENSHOT_PATH,
                SCREENSHOT_NAMES.get(genre),
            )

        changed = dash_to_underscore(new_datas)
        self.store_videoid_to_sqlite(changed)

    def init_logger(self, show_logs: bool):
        general_log = f"{LOG_PATH}{LOG_NAME}"
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # file_handler_formatter = logging.Formatter(
        #     "%(levelname)s [%(asctime)s] [%(username)s]  %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        # )

        # console_handler_formatter = logging.Formatter(
        #     "%(levelname)s [%(asctime)s] [%(username)s]  %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        # )

        file_handler_formatter = logging.Formatter()
        # console_handler_formatter = logging.Formatter()

        # TODO :
        # 두 번 할당하는건 뭐지?
        file_handler = logging.FileHandler(general_log)
        # file_handler = RotatingFileHandler(
        #     general_log, maxBytes=10 * 1024 * 1024, backupCount=5
        # )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_handler_formatter)

        logger.addHandler(file_handler)

        # TODO :
        # if custom_log_handler:
        #     logger.addHandler(custom_log_handler)

        # TODO :
        if show_logs:
            pass
        #     console_handler = logging.StreamHandler()
        #     console_handler.setLevel(logging.DEBUG)
        #     console_handler.setFormatter(console_handler_formatter)
        #     logger.addHandler(console_handler)

        return logger
