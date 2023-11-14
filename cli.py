"""
Movie Recommender

Usage:
  movirecommender <number_movies> <file_path>
  movirecommender -h | --help
  movirecommender --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Arguments:
  number_movies - number of movies
  file_path - JSON file path

Example:
  movirecommender 5 /home/user/movies.json

Help:
  It recommends movies based on movies that users have already watched.
  This program accepts two arguments: number of movies that you want to be
  recommended and the file with the movies and users information.
  The json file has to have the following structure:
  {
    "movies": {
        <movie_id:str>: <movie_name:str>,
    },
    "users": [
        {
            "movies": [
                <movie_id:int>,
            ],
            "user_id": <user_id:int>
        },
    ]
  }
"""


from docopt import docopt
from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import recommender
    import os.path
    options = docopt(__doc__, version=VERSION)
    if options['<number_movies>'] and options['<file_path>']:
        try:
            n_movies = int(options['<number_movies>'])
        except ValueError:
            return '[ERROR]: You have to insert a number for <number_movies>!'
        if os.path.exists(options['<file_path>']):
            json_file = options['<file_path>']
            recommender.run(n_movies, json_file)
        else:
            return '[ERROR]: The file given does not exist!'