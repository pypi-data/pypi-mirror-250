from cria_index.core.readers.base import BaseLoader

class GmailLoader(BaseLoader):
    @classmethod
    def class_name(cls):
        return "GmailLoader"