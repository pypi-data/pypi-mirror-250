import os
from typing import AnyStr

from py_temporal_doc.base_types.cls.parser import Parser
from py_temporal_doc.commands.command import Command
from py_temporal_doc.commands.consts import JSON_FILE_NAME


class GenerateJSON(Command):
    def __init__(self, parser: Parser):
        self.__parser = parser

    """
    Class for generating diagram
    """

    def __read_file(self, file_path: str):
        if not file_path.lower().endswith(".py"):
            # print(f"{file_path} is not a python file. Skipping...")
            return

        with open(file_path) as file:
            try:
                df: AnyStr = file.read()
                # Parse here
                self.__parser.parse(df, file_path)
            except Exception:
                # print(f"Unable to parse: {file_path}. Skipping...")
                pass

    def __read_directory(self, path: str):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                self.__read_file(subdir + "/" + file)

    def execute(self, **kwargs) -> None:
        """
        Execute generate diagram entry point

        Args:
            **kwargs: arguments from CLI

        Returns:
            None
        """

        if "source" in kwargs and "destination" in kwargs:
            source: str = kwargs["source"]
            destination: str = kwargs["destination"]

            if os.path.isdir(source):
                self.__read_directory(source)
            elif os.path.isfile(source):
                self.__read_file(source)

        # Creates relationship ties for all saved nodes
        resp: str = self.__parser.get_json()
        # print(resp)  # TODO: Remove once finalized

        # If the file doesn't exist, it will be created. If it exists, its content will be overwritten.
        with open(f"{destination}/{JSON_FILE_NAME}", 'w') as file:
            file.write(resp)

        print("Generate JSON done")
