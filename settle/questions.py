"""
Function to ask questions and get answers
"""
import inquirer
from inquirer.themes import load_theme_from_dict

from .distros import DISTROS_PACKAGE_MANAGERS, PACKAGE_MANAGERS


# Define a custom theme for Inquirer
INQUIRER_THEME = {
    "Question": {
        "mark_color": "yellow",
        "brackets_color": "normal",
        "default_color": "normal",
    },
    "Editor": {"opening_prompt_color": "bright_black"},
    "Checkbox": {
        "selection_color": "normal",
        "selection_icon": ">",
        "selected_icon": "[x]",
        "selected_color": "bold_yellow",
        "unselected_color": "normal",
        "unselected_icon": "[ ]",
    },
    "List": {
        "selection_color": "blue",
        "selection_cursor": ">",
        "unselected_color": "normal",
    },
}


class Asker:
    """
    Ask questions to know which actions must be performed
    """

    def __init__(
        self, packages_dict, default_categories, package_manager, list_packages=False
    ):
        self.packages_dict = packages_dict
        self.default_categories = default_categories
        self.package_manager = package_manager
        self.list_packages = list_packages
        # Create questions
        self.questions = self.create_questions()

    def ask_questions(self):
        """
        Ask questions
        """
        # Ask questions
        answers = inquirer.prompt(self.questions, theme=self.inquirer_theme)
        # Create list of chosen packages if any category has been chosen
        answers["install_packages"] = self.get_install_packages_list(answers)
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
        questions.append(self.update_packages_question)
        if self.list_packages:
            questions.append(self.choose_packages_question)
        else:
            questions.append(self.choose_categories_question)
        questions.append(self.confirmation)
        return questions

    def get_install_packages_list(self, answers):
        """
        Create the list of all packages that must be installed

        The list of all packages that must be installed is created after the answers
        recovered from the Asker instance.
        """
        install_packages = []
        if "categories" in answers:
            for category in answers["categories"]:
                install_packages += self.packages_dict[category]
        elif "packages" in answers:
            install_packages = answers["packages"]
        return install_packages

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
        # Get list of all packages and the packages inside the default categories
        all_packages = []
        default_packages = []
        for category, packages in self.packages_dict.items():
            all_packages += packages
            if category in self.default_categories:
                default_packages += packages
        # Create question
        question = inquirer.Checkbox(
            "packages",
            message="What packages do you want to install?",
            choices=all_packages,
            default=default_packages,
        )
        return question

    @property
    def choose_categories_question(self):
        """
        Return question about which packages should be installed based on categories
        """
        question = inquirer.Checkbox(
            "categories",
            message="What packages do you want to install?",
            choices=list(self.packages_dict.keys()),
            default=self.default_categories,
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
