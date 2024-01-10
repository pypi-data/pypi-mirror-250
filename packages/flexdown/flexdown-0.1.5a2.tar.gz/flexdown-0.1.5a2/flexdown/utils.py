"""Utility functions for Flexdown."""

import os
import re

from flexdown import constants, errors, types


def get_flexdown_files(path: str) -> list[str]:
    """Recursively get the Flexdown files in a directory.

    Args:
        path: The path to the directory to search.

    Returns:
        The list of Flexdown files in the directory.
    """
    flexdown_files = []
    for root, _, files in os.walk(path):
        flexdown_files.extend(
            [
                os.path.join(root, file)
                for file in files
                if file.endswith(constants.FLEXDOWN_EXTENSION)
            ]
        )
    return flexdown_files


def evaluate_templates(line: str, env: types.Env):
    """Evaluate template expressions in a line of text.

    Args:
        line: The line of text to evaluate.
        env: The environment variables to use for evaluation.
    """
    # Find all template placeholders in the line.
    matches = re.findall(constants.TEMPLATE_REGEX, line)

    # Iterate over each template placeholder.
    for match in matches:
        try:
            # Evaluate the Python expression and replace the template placeholder
            eval_result = str(eval(match, env, env))
            line = line.replace("{" + match + "}", eval_result)
        except Exception as e:
            # If the evaluation fails, leave the template placeholder unchanged
            raise errors.TemplateEvaluationError(
                f"Failed to evaluate expression '{match}'"
            ) from e

    # Return the line with the template placeholders replaced.
    return line
