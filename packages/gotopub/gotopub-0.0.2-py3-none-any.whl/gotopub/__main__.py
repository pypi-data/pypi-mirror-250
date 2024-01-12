# GoToPub - GoToSocial and general Fediverse client
# Copyright (C) 2024  András Németh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""GoToPub"""

# imports: library
from argparse import ArgumentParser

# imports: dependencies
from libmonty_logging.config.file_and_stream.v1 import config as logging_config
import libmonty_logging.helper as logging_helper
import libmonty_logging.message as logging_message

# imports: project
from gotopub import version


def main() -> None:
    """Main"""

    logging_helper.apply_config(version.PROGRAM_NAME,
                                version.__version__,
                                logging_config)

    logging_message.program_header(version.PROGRAM_NAME)

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    args = parser.parse_args()

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return


if __name__ == '__main__':
    main()
