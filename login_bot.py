"""Automate login to the CEDSa Postítulos campus page.

This script opens the login page, fills the username and password fields with
values loaded from a credentials file, and clicks the "Acceder" button. After
signing in it opens the "Diplomatura Superior en Programación y Robótica" course
page and alternates every 10 minutes between the course home and its Module 1
section until the browser is closed.

The credentials file must contain two lines in the form:

    username=<your username>
    password=<your password>

Example usage::

    python login_bot.py credentials.txt

By default the browser runs in headless mode. Pass ``--show`` to see the
browser window.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Tuple

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

LOGIN_URL = "https://campusvirtual.cedsa.edu.ar/postitulo/login/index.php"
COURSE_HOME_URL = (
    "https://campusvirtual.cedsa.edu.ar/postitulo/course/view.php?id=94"
)
MODULE_ONE_URL = (
    "https://campusvirtual.cedsa.edu.ar/postitulo/course/view.php?id=94&section=4"
)
RECOVERY_MODULE_URL = (
    "https://campusvirtual.cedsa.edu.ar/postitulo/course/view.php?id=94&section=3"
)
ASSIGNMENT_URL = (
    "https://campusvirtual.cedsa.edu.ar/postitulo/mod/assign/view.php?id=16088"
)
TEN_MINUTES_SECONDS = 10 * 60
USERNAME_FIELD_ID = "username"
PASSWORD_FIELD_ID = "password"
LOGIN_BUTTON_ID = "loginbtn"


def load_credentials(path: Path) -> Tuple[str, str]:
    """Load username and password from ``path``.

    The file must contain ``username`` and ``password`` entries separated by an
    equals sign, one per line. Blank lines and comments starting with ``#`` are
    ignored.
    """
    username = password = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise ValueError(
                f"Invalid line in credentials file {path!s}: {line!r}."
                " Expected 'key=value'."
            )
        key, value = (item.strip() for item in stripped.split("=", 1))
        if key == "username":
            username = value
        elif key == "password":
            password = value

    if not username or not password:
        raise ValueError(
            "Credentials file must define both 'username' and 'password'."
        )

    return username, password


def create_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome WebDriver instance.

    When ``headless`` is True, the browser runs without opening a window.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def login(credentials_path: Path, headless: bool = True) -> None:
    """Automate the login process using the supplied credentials file."""
    username, password = load_credentials(credentials_path)

    driver = create_driver(headless=headless)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(LOGIN_URL)

        username_input = wait.until(
            EC.presence_of_element_located((By.ID, USERNAME_FIELD_ID))
        )
        password_input = wait.until(
            EC.presence_of_element_located((By.ID, PASSWORD_FIELD_ID))
        )
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, LOGIN_BUTTON_ID))
        )

        username_input.clear()
        username_input.send_keys(username)

        password_input.clear()
        password_input.send_keys(password)

        login_button.click()

        # Optionally wait for navigation or additional steps here.
        wait.until(lambda drv: drv.current_url != LOGIN_URL)
        print("Login attempt submitted.")

        driver.get(COURSE_HOME_URL)
        wait.until(EC.url_to_be(COURSE_HOME_URL))
        print("Opened the diplomatura course page.")

        driver.get(RECOVERY_MODULE_URL)
        wait.until(EC.url_to_be(RECOVERY_MODULE_URL))
        print("Opened the recovery module page.")

        driver.get(ASSIGNMENT_URL)
        wait.until(EC.url_to_be(ASSIGNMENT_URL))
        print(
            "Opened the assignment page. Waiting 10 seconds before starting the navigation loop..."
        )
        time.sleep(10)

        driver.get(COURSE_HOME_URL)
        wait.until(EC.url_to_be(COURSE_HOME_URL))

        print(
            "Starting 10-minute navigation loop between the course home and Module 1."
        )
        print(
            "Close the browser window or press Ctrl+C in the terminal to stop the script."
        )

        try:
            while True:
                print("Waiting 10 minutes on the course home page before visiting Module 1...")
                time.sleep(TEN_MINUTES_SECONDS)

                driver.get(MODULE_ONE_URL)
                wait.until(EC.url_to_be(MODULE_ONE_URL))
                print("Module 1 opened. Waiting 10 minutes before returning to the course home...")

                time.sleep(TEN_MINUTES_SECONDS)

                driver.get(COURSE_HOME_URL)
                wait.until(EC.url_to_be(COURSE_HOME_URL))
                print("Returned to the course home page.")
        except KeyboardInterrupt:
            print("Navigation loop interrupted by user.")
        except WebDriverException as exc:
            print(
                "WebDriver reported an issue (browser may have been closed):"
                f" {exc}"
            )
    finally:
        driver.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "credentials",
        type=Path,
        help="Path to the credentials file (username=..., password=...).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Run the browser with a visible window instead of headless mode.",
    )
    args = parser.parse_args()

    login(args.credentials, headless=not args.show)


if __name__ == "__main__":
    main()
