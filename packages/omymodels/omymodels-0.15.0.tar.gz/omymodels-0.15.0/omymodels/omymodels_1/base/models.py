from abc import ABC, abstractmethod
from .mixins import EqualByNameMixIn
from typing import Dict, List, Optional
from table_meta import TableMeta
from .utils import ModelsParsingException


sql_file_formats = ['sql', 'ddl', 'hql']


class FileFormats:
    # by default those formats supported in Omymodels default parser
    sql: List[str] = sql_file_formats
    python: List[str] = ['py']

    
class BaseProvider(ABC, EqualByNameMixIn):

    name = 'base-provider'

    def __init_subclass__(cls, /, **kwargs):
        if not getattr('type', None):
            raise ValueError("Provider should have a class variable 'type' with one of possible types `generator` or `parser`")
        if not getattr('name', None):
            raise ValueError("Provider should have a class variable 'name' with user-friendly name of Provider")
        if not isinstance(cls.name, str):
            raise ValueError("`name` variable of Provider class should have a string type")
        if cls.name == cls.mro()[1].name and cls.__name__ != cls.mro()[1].__name__:
            raise ValueError("You should define `name` class variable in your Provider class. "
                             "Name should be user friendly and will be used to choose provider with config")
        super().__init_subclass__(**kwargs)

    @abstractmethod
    def run(self, input, params):
        raise NotImplementedError(
            'Each Provider - Parser, Generator or Converter should have '
            '`run` method that takes some input and params to run with.'
        )


class BaseParser(BaseProvider):

    type = 'parser'
    name = 'base-parser'

    supported_file_formats = FileFormats.sql + FileFormats.python

    def __init_subclass__(cls, /, **kwargs):
        if not getattr('supported_file_formats', None) or not isinstance(cls.supported_file_formats, list):
            raise ValueError("Parser should have a class variable 'supported_file_formats' that should contains a list "
                             "of strings with supported file formats prefixes, for example: ['sql', 'ddl', 'py']")

        super().__init_subclass__(**kwargs)

    def execute(self, input: str, params: Dict) -> TableMeta:
        """ should be implemented in parser """
        raise NotImplementedError
    
    def validate_input(self, 
                       input: Input
                       ):
        if not input_path and not input:
            raise ModelsParsingException("To parse models you should provide a path to the file or folder with models")
        
    def run(
        self, 
        params: Dict, 
        input_path: Optional[str] = None, 
        input: Optional[str] = None,
        input_format: Optional[str] = None,
        exclude: Optional[str] = None):
        """ input of parser: str context of parsed input - python module with models or ddl-file 
            params: dict with any params that can be used in Parser Provider """
        
        self.validate_input(input_path, input_format, input_format, exclude)
        # implement this method in your parser provider
        
        return self.execute(input)


class BaseGenerator(BaseProvider):

    type = 'generator'
    name = 'define-name-of-your-generator'

    def run(self, input: TableMeta, params):
        # implement this method in your generator provider
        
        raise NotImplementedError
