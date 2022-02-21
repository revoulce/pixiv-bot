import logging

from telegram.ext import CommandHandler, Updater

from Singleton import Singleton

logger = logging.getLogger(__name__)


class Bot(metaclass=Singleton):
    def __init__(self, token, admin_id):
        self.handlers = []
        self.updater = Updater(token=token)
        self.token = token
        self.admin_id = admin_id

        for x in dir(self):
            if not x.startswith("__"):
                attr = getattr(self, x)
                if hasattr(attr, "_command_options"):
                    logger.debug("Adding %s to handlers", attr)
                    logger.debug("Command options: %s", attr._command_options)
                    self.handlers.append(CommandHandler(command=attr.__name__, callback=attr, *attr._command_options[
                        0], **attr._command_options[1]))

        dispatcher = self.updater.dispatcher
        for h in self.handlers:
            dispatcher.add_handler(h)

    def __del__(self):
        logger.debug("Closing %s", self.__name__)
