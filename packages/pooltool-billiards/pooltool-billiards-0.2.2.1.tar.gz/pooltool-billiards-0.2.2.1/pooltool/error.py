#! /usr/bin/env python

"""Borrowed from https://github.com/merenlab/anvio/blob/master/anvio/errors.py"""

import textwrap

from pooltool.terminal import color_text


def remove_spaces(text):
    if not text:
        return ""

    while True:
        if text.find("  ") > -1:
            text = text.replace("  ", " ")
        else:
            break

    return text


class PoolToolError(Exception):
    def __init__(self, e=None):
        Exception.__init__(self)
        return

    def __str__(self):
        max_len = max([len(line) for line in textwrap.fill(self.e, 80).split("\n")])
        error_lines = [
            "%s%s" % (line, " " * (max_len - len(line)))
            for line in textwrap.fill(self.e, 80).split("\n")
        ]

        error_message = [
            "%s: %s" % (color_text(self.error_type, "red"), error_lines[0])
        ]
        for error_line in error_lines[1:]:
            error_message.append(
                "%s%s" % (" " * (len(self.error_type) + 2), error_line)
            )

        return "\n\n" + "\n".join(error_message) + "\n\n"

    def clear_text(self):
        return self.e


class ConfigError(PoolToolError):
    def __init__(self, e=None):
        self.e = remove_spaces(e)
        self.error_type = "Config Error"
        PoolToolError.__init__(self)


class StrokeError(PoolToolError):
    def __init__(self, e=None):
        self.e = remove_spaces(e)
        self.error_type = "Stroke Error"
        PoolToolError.__init__(self)


class SimulateError(PoolToolError):
    def __init__(self, e=None):
        self.e = remove_spaces(e)
        self.error_type = "Simulate Error"
        PoolToolError.__init__(self)
