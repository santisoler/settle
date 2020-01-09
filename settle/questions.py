"""
Function to ask questions and get answers
"""
import inquirer
from inquirer.themes import load_theme_from_dict

from .distros import DISTROS_PACKAGE_MANAGERS, PACKAGE_MANAGERS
from .utils import check_valid_default_packages


# Define a custom theme for Inquirer
INQUIRER_THEME = {
    "Question": {
        "mark_color": "yellow",
        "brackets_color": "normal",
        "default_color": "normal",
    },
    "Editor": {
        "opening_prompt_color": "bright_black",
    },
    "Checkbox": {
        "selection_color": "normal",
        "selection_icon": '>',
        "selected_icon": '[x]',
        "selected_color": "bold_yellow",
        "unselected_color": "normal",
        "unselected_icon": '[ ]',
    },
    "List": {
        "selection_color": "blue",
        "selection_cursor": ">",
        "unselected_color": "normal",
    }
}


class Asker():
    """
    Ask questions to know which actions must be performed
    """

    def __init__(self, packages, package_manager):
        self.packages = packages
        self.package_manager = package_manager
        self.default_packages = []
        # Pop default categories
        self._pop_default_packages()
        # Create questions
        self.questions = self.create_questions()

    def ask_questions(self):
        """
        Ask questions
        """
        # Ask questions
        answers = inquirer.prompt(self.questions, theme=self.inquirer_theme)
        # Create list of chosen packages if any category has been chosen
        answers["install_packages"] = []
        if answers["categories"]:
            for group in answers["categories"]:
                answers["install_packages"] += self.packages[group]
        return answers

    def create_questions(self):
        """
        Create all inquirer questions
        """
        questions = []
        # Ask which package manager should we use if it's None
        if self.package_manager is None:
            questions.append(self.package_manager_question)
        # Add more questions
        questions += [
            self.update_packages_question,
            self.choose_packages_question,
            self.confirmation,
        ]
        return questions

    def _pop_default_packages(self):
        """
        Pop the default section and define default_packages attribute
        """
        if "default" in self.packages:
            self.default_packages = self.packages.pop("default")
            check_valid_default_packages(self.packages, self.default_packages)

    @property
    def inquirer_theme(self):
        return load_theme_from_dict(INQUIRER_THEME)

    @property
    def package_manager_question(self):
        """
        Return question asking about what package manager should we use
        """
        question = inquirer.List(
            "package_manager",
            message="What package manager should we use?",
            choices=PACKAGE_MANAGERS,
        )
        return question

    @property
    def update_packages_question(self):
        """
        Return question for updating packages
        """
        question = inquirer.Confirm(
            "update_packages",
            message="Do you want to update all packages?",
            default=True,
        )
        return question

    @property
    def choose_packages_question(self):
        """
        Return question about which packages should be installed
        """
        question = inquirer.Checkbox(
            "categories",
            message="What packages do you want to install?",
            choices=list(self.packages.keys()),
            default=self.default_packages,
        )
        return question

    @property
    def confirmation(self):
        """
        Return confirmation question
        """
        question = inquirer.Confirm(
            "continue",
            message="Do you really want to perform the chosen tasks?",
            default=True,
        )
        return question
