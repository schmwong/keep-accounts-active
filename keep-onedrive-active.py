# pip install playwright
# playwright install firefox
# pip install python-dotenv

import sys

sys.dont_write_bytecode = True

import os
from playwright.sync_api import sync_playwright, TimeoutError
from logging_formatter import Year
from login_logger import LoginLogger
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------- #
# Initialising Microsoft OneDrive instances
# Enclose them in functions to be called later
# Instantiate only at runtime to prevent concurrent runs

onedrive = "https://onedrive.live.com"
onedrive_signin = "https://onedrive.live.com/about/en-gb/signin/"
onedrive_usr_sel = "input.form-control"
onedrive_pwd_sel = "input.form-control"
onedrive_homepage = "https://onedrive.live.com/?gologin=1&mkt=en%2DGB"
iframe_sel = "iframe.SignIn"


def mkfilename(a):
    filename = f"[{Year}] {a} log.csv"
    return filename


def onedrive_1():
    instance = LoginLogger(
        base_url=onedrive,
        login_url=onedrive_signin,
        usr_sel=onedrive_usr_sel,
        usr=os.getenv("USR_ONEDRIVE_1"),
        pwd_sel=onedrive_pwd_sel,
        pwd=os.getenv("PWD_ONEDRIVE_1"),
        homepage=onedrive_homepage,
        filename=mkfilename("onedrive_1"),
    )
    return instance


def onedrive_2():
    instance = LoginLogger(
        base_url=onedrive,
        login_url=onedrive_signin,
        usr_sel=onedrive_usr_sel,
        usr=os.getenv("USR_ONEDRIVE_2"),
        pwd_sel=onedrive_pwd_sel,
        pwd=os.getenv("PWD_ONEDRIVE_2"),
        homepage=onedrive_homepage,
        filename=mkfilename("onedrive_2"),
    )
    return instance


#
# ----------------------------------- #

# =================================== #
# Optional scraper script
#
def query_onedrive_storage(instance):
    page = instance.tab
    logger = instance.logger

    logger.info(f"Getting storage details from '{instance.dashboard_url}'")
    page.wait_for_timeout(2529)

    name = page.query_selector(
        "div#O365_HeaderRightRegion span[style='display: none;']"
    ).inner_text()

    email = instance.usr

    plan = page.query_selector(
        """div:nth-child(5) > table > tbody > tr.StorageInfo-plans-row > td.StorageInfo-plans-type-text-cell > span > span"""
    ).inner_text()

    storage_name = page.query_selector("div.StorageInfo-totalUsed").inner_text()
    storage_used = page.query_selector("div.od-quota-progress-bar-main").inner_text()

    logger.debug(f"Profile name: {name}")
    logger.debug(f"Email: {email}")
    logger.debug(f"Plan: {plan}")
    logger.debug(f"{storage_name}: {storage_used}")
    #
    # =================================== #


def onedrive_login(instance):
    with sync_playwright() as pw:
        logger = instance.logger
        instance.iframe_login(pw, iframe_sel)
        instance.redirect(href_sel="a.od-QuotaBar-link")
        query_onedrive_storage(instance)
        logger.info("Tasks complete. Closing browser")
        # Remove FileHandlder to prevent reopening the previous instance's file in the next instance
        # due to the Class Variable getting recreated during "self.logger.addHandler(self.DuoHandler)"
        logger.removeHandler(instance.DuoHandler)


if __name__ == "__main__":
    onedrive_login(onedrive_1())
    onedrive_login(onedrive_2())
