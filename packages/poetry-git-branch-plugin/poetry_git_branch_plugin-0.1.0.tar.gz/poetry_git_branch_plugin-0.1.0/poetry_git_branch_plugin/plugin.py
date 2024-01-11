import os

from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PoetryGitBranchPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(COMMAND, self.set_git_branch_env_var)

    def set_git_branch_env_var(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        if not isinstance(event.command, EnvCommand):
            return

        env_var = "POETRY_GIT_BRANCH"
        # event.io.write_line(f"Setting {env_var} environment variable...")
        os.environ[env_var] = os.popen("git symbolic-ref --short HEAD").read().strip()
