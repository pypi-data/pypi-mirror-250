# SPDX-FileCopyrightText: 2023-present Artem Lykhvar <me@a10r.com>
#
# SPDX-License-Identifier: MIT
import os
import subprocess
import sys
from functools import partial
from pathlib import Path

from click import Group, pass_context, secho, version_option

if sys.version_info >= (3, 11):
    import tomllib  # no cov
else:
    import tomli as tomllib  # no cov


context_settings = {
    "help_option_names": [],
    "ignore_unknown_options": True,
}


class App(Group):
    def __init__(self, config=None):
        super().__init__()
        self.config = config or Path(os.getcwd(), "pyproject.toml")
        self.commands = self._commands()
        self.invoke_without_command = True
        self.no_args_is_help = (True,)
        self.chain = True

    @staticmethod
    def _execute(cmd, ctx):  # noqa: ARG004
        for entry in cmd:
            secho(f"\n => {entry}")
            subprocess.call(entry, shell=True)  # noqa: S602

    @classmethod
    def _unfold(cls, cmd, entries):
        for sub in cmd:
            if sub in entries:
                cmd = entries.get(sub)
                if isinstance(cmd, list) and not isinstance(cmd, str):
                    yield from cls._unfold(cmd, entries)
                else:
                    yield cmd
            else:
                yield sub

    @staticmethod
    def _abort(message):
        secho(message, err=True, fg="red")
        raise SystemExit(0)

    def _read_config(self, entry="cli"):
        if not self.config.exists():
            self._abort("No pyproject.toml file found")
        try:
            with open(self.config, encoding="utf-8") as f:
                try:
                    config = tomllib.loads(f.read())
                    return config["tool"].get(entry, {})
                except KeyError:
                    self._abort("No configuration found at pyproject.toml")
        except OSError as err:
            self._abort(f"Error loading configuration: {err}")

    def _commands(self):
        commands, entries = {}, self._read_config()

        for name, entry in entries.items():
            cmd = [entry] if isinstance(entry, str) else entry
            if name in cmd:
                self._abort("Command error. Command can't rely on itself.")

            commands[name] = self.command(
                name=name,
                short_help=" && ".join(cmd),
                context_settings=context_settings,
            )(pass_context(partial(self._execute, self._unfold(cmd, entries))))

        return commands


app = version_option()(App())
