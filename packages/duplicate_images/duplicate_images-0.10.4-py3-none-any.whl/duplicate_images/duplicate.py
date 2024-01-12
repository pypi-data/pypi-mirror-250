#!/usr/bin/env /usr/bin/python3

import logging
from argparse import Namespace
from os import walk, access, R_OK
from pathlib import Path
from typing import Callable, List, Optional

from filetype import guess
from pillow_heif import register_heif_opener

from duplicate_images.common import path_with_parent
from duplicate_images.function_types import Results
from duplicate_images.hash_store import FileHashStore
from duplicate_images.image_pair_finder import ImagePairFinder, PairFinderOptions
from duplicate_images.log import setup_logging
from duplicate_images.methods import ACTIONS_ON_EQUALITY, IMAGE_HASH_ALGORITHM, get_hash_size_kwargs
from duplicate_images.parse_commandline import parse_command_line

register_heif_opener()


def is_image_file(filename: Path) -> bool:
    """Returns True if filename is a readable image file"""
    if access(filename, R_OK) and not filename.is_symlink():
        kind = guess(filename)
        return kind is not None and kind.mime.startswith('image/')
    return False


def files_in_dirs(
        dir_names: List[Path], is_file: Callable[[Path], bool] = lambda f: f.is_file()
) -> List[Path]:
    """Returns a list of all files in directory dir_name, recursively scanning subdirectories"""
    files = [
        Path(root) / filename
        for dir_name in dir_names
        for root, _, filenames in walk(dir_name)
        for filename in filenames
        if is_file(Path(root) / filename)
    ]
    return files


def get_matches(
        root_directories: List[Path], algorithm: str,
        options: PairFinderOptions = PairFinderOptions(),
        hash_store_path: Optional[Path] = None
) -> Results:
    hash_algorithm = IMAGE_HASH_ALGORITHM[algorithm]
    hash_size_kwargs = get_hash_size_kwargs(hash_algorithm, options.hash_size)
    image_files = sorted(files_in_dirs(root_directories, is_image_file))
    logging.info('%d total files', len(image_files))
    logging.info('Computing image hashes')

    with FileHashStore.create(hash_store_path, algorithm, hash_size_kwargs) as hash_store:
        return ImagePairFinder.create(
            image_files, hash_algorithm, options=options, hash_store=hash_store,

        ).get_equal_groups()


def execute_actions(matches: Results, args: Namespace) -> None:
    action_equal = ACTIONS_ON_EQUALITY[args.on_equal]
    for group in sorted(matches):
        try:
            action_equal(args, group)
        except FileNotFoundError:
            continue


def main() -> None:
    args = parse_command_line()
    setup_logging(args)
    options = PairFinderOptions.from_args(args)
    for folder in args.root_directory:
        logging.info('Scanning %s', path_with_parent(folder))
    try:
        matches = get_matches(
            [Path(folder) for folder in args.root_directory], args.algorithm,
            options=options, hash_store_path=Path(args.hash_db) if args.hash_db else None
        )
        logging.info('%d matches', len(matches))
        execute_actions(matches, args)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
