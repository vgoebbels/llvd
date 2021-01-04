# !/usr/bin/env  python3

import click
import sys
import re
from llvd.app import App
from llvd import config
from pathlib import Path
import os
from os import access, R_OK
from os.path import isfile
import configparser

BOLD = "\033[1m"  # Makes the text bold
RED_COLOR = "\u001b[31m"  # Makes the text red
CONF_FILE_NAME = ".llvd"


@click.command()
@click.option("--resolution", "-r",
              default='720',
              help='Video resolution can either be 360, 540 or 720. 720 is the default')
@click.option("--course", "-c", help="Example: 'Java 8 Essential'")
def main(course, resolution):
    """
    Linkedin learning video downloader cli tool

    example: llvd --course "Java 8 Essential"

    Login credentials can be put in ~/.llvd (optional!)

    Example:

        [login]

        email=<EMAIL>

        password=<PASSWORD>
    """
    conf_file = str(Path.home()) + os.path.sep + CONF_FILE_NAME
    if isfile(conf_file) and access(conf_file, R_OK):
        config = configparser.ConfigParser()
        config.read(conf_file)
        email = config.get('login', 'email', fallback='')
        password = config.get('login', 'password', fallback='')

    if len(sys.argv) == 1:
        click.echo(f"{RED_COLOR}{BOLD}Missing required arguments: llvd --help")
        sys.exit(0)

    course = re.sub("[)|(|,]|(-&)", "", course.lower())

    course_slug = course.replace(" ", "-").replace(":-", "-").replace(
        "-&", ""
    ).replace(".", "-")
    if len(email)==0:
        email = click.prompt("Please enter your Linkedin email address")
    if len(password)==0:
        password = click.prompt("Enter your Linkedin Password", hide_input=True)

    llvd = App(email, password, course_slug, resolution)
    llvd.run()
