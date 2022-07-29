import sys

sys.dont_write_bytecode = True

import os
import logging
from logging_formatter import CsvFormatter


class LoginLogger:
    def __init__(
        self, base_url, login_url, usr_sel, usr, pwd_sel, pwd, homepage, filename
    ):
        # --- From params --- #
        self.url = base_url
        self.login_url = login_url
        self.usr_sel = usr_sel
        self.usr = usr
        self.pwd_sel = pwd_sel
        self.pwd = pwd
        self.homepage = homepage  # landing page upon logging in
        self.filename = filename
        # ------------------- #

        self.dashboard_url = None
        self.tab = None  # To store playwright Page class instance

        self.formatter = CsvFormatter(self.filename)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.DuoHandler = logging.StreamHandler()
        self.DuoHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.DuoHandler)

    def one_step_login(self, playwright):
        logger = self.logger
        logger.info("Launching browser")
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(self.login_url)
        logger.info(f"Retrieving login page '{self.login_url}'")
        page.fill(self.usr_sel, self.usr)
        page.fill(self.pwd_sel, self.pwd)
        page.keyboard.press("Enter")
        logger.info("Logging in")
        page.wait_for_url(self.homepage, wait_until="domcontentloaded", timeout=120_000)
        logger.info("Logged in successfully")
        self.tab = page

    def two_step_login(self, playwright, captcha_page=None, pwd_page=None):
        logger = self.logger
        logger.info("Launching browser")
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(self.login_url)
        logger.info(f"Retrieving login page '{self.login_url}'")
        page.fill(self.usr_sel, self.usr)
        page.keyboard.press("Enter")
        if captcha_page is not None:
            try:
                page.wait_for_url(
                    captcha_page + "**", wait_until="domcontentloaded", timeout=10_000
                )
                page.keyboard.press("Tab")
                page.keyboard.press("Tab")
                page.keyboard.press("Tab")
                page.keyboard.press("Enter")
                page.keyboard.press("Tab")
                page.keyboard.press("Tab")
                page.keyboard.press("Tab")
                page.keyboard.press("Enter")
            except:
                pass
        if pwd_page is not None:
            try:
                page.wait_for_url(
                    pwd_page + "**", wait_until="domcontentloaded", timeout=10_000
                )
            except:
                pass
        page.fill(self.pwd_sel, self.pwd, timeout=10_000)
        page.keyboard.press("Enter")
        logger.info("Logging in")
        page.wait_for_url(self.homepage + "**")
        page.wait_for_load_state("domcontentloaded")
        logger.info("Logged in successfully")
        self.tab = page

    def iframe_login(self, playwright, frame_locator, **kwargs):
        logger = self.logger
        logger.info("Launching browser")
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(self.login_url)
        logger.info(f"Retrieving login page '{self.login_url}'")
        page.wait_for_url(self.login_url, wait_until="domcontentloaded")
        frame = page.frame_locator(frame_locator).locator(self.usr_sel)
        frame.fill(self.usr)
        page.keyboard.press("Enter")
        page.fill(self.pwd_sel, self.pwd)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2529)
        page.keyboard.press("Enter")
        logger.info("Logging in")
        page.wait_for_url(self.homepage + "**", wait_until="domcontentloaded")
        logger.info("Logged in successfully")
        self.tab = page

    def redirect(self, **kwargs):
        logger = self.logger
        page = self.tab
        if "href_sel" in kwargs:
            self.dashboard_url = self.url + page.locator(
                kwargs.get("href_sel")
            ).get_attribute("href")
        elif "url" in kwargs:
            self.dashboard_url = kwargs.get("url")
        page.goto(self.dashboard_url)
        page.wait_for_timeout(2529)


# def rename_file(new_name):
#     year = Year

#     # open("temp.csv").close()  # file was kept open while writing logs
#     new_filename = f"[{year}] {new_name}.csv"
#     cols = ["Date", "Time", "Level", "Message"]

#     def execute(action):
#         with open("temp.csv", "r") as infile, open(
#             new_filename, action, newline=""
#         ) as outfile:
#             writer = DictWriter(outfile, fieldnames=cols, extrasaction="ignore")
#             reader = DictReader(infile)
#             for row in reader:
#                 if "Using selector:" not in row["Message"]:
#                     writer.writerow(row)
#                     print(row)

#     if os.path.isfile(new_filename):
#         execute("a")
#         os.remove("temp.csv")
#     else:
#         execute("w")
#         os.remove("temp.csv")
