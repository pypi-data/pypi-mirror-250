from cria_index.core.readers.base import BaseLoader

class NotionLoader(BaseLoader):
    @classmethod
    def class_name(cls):
        return "NotionLoader"