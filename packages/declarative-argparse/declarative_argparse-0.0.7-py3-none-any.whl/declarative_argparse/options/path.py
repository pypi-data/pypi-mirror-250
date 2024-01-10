from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional
import typing

from declarative_argparse.options.abc import IDeclarativeOption

if typing.TYPE_CHECKING:
    from declarative_argparse import DeclarativeOptionParser

class PathDO(IDeclarativeOption):
    def __init__(self, dop: 'DeclarativeOptionParser', *flags: List[str], description: Optional[str] = None) -> None:
        super().__init__(dop, *flags, description=description)
        self.checkDirectoryExists: bool = False
        self.checkFileExists: bool = False

    def get_value(self) -> Optional[Path]:
        o = super().get_value()
        if o is None:
            return None
        return o

    def handle_input(self, arg_content: str) -> Any:
        v = Path(arg_content)
        if self.checkDirectoryExists:
            assert v.is_dir(), f'{v} does not exist as a directory!'
        if self.checkFileExists:
            assert v.is_file(), f'{v} does not exist as a file!'
        return v


    def ensureIsAFile(self) -> PathDO:
        self.checkFileExists = True
        return self

    def ensureIsADirectory(self) -> PathDO:
        self.checkDirectoryExists = True
        return self


class PathArrayDO(IDeclarativeOption):
    def __init__(self, dop: 'DeclarativeOptionParser', *flags: List[str], check_directories_exist: bool=False, check_files_exist: bool=False,description: Optional[str] = None) -> None:
        super().__init__(dop, *flags, description=description)
        self.checkDirectoryExists: bool = check_directories_exist
        self.checkFileExists: bool = check_files_exist

    def get_value(self) -> Optional[List[Path]]:
        o = super().get_value()
        if o is None:
            return None
        return [Path(e) for e in o]

    def handle_input(self, arg_content: str) -> Any:
        return Path(arg_content)

    def ensureAreAllFiles(self) -> PathArrayDO:
        self.checkFileExists = True
        return self

    def ensureAreAllDirs(self) -> PathArrayDO:
        self.checkDirectoryExists = True
        return self
