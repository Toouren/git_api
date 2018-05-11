import requests
import re
import argparse


class GitApi:
    def __init__(self, name):
        self.username = name
        self.next_url_pattern = re.compile('<(.*)>; rel=\"next\"')
        self.repeated_next_url_pattern = re.compile(', <(.*)>; rel=\"next\"')
        self.last_url_patter = re.compile(', <(.*)>; rel=\"last\"')
        self.result = dict()

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('name', nargs='?')
        return parser

    def collect_info(self, repos):
        for repo in repos:
            self.result[repo['name']] = repo['stargazers_count']

    def run(self):
        try:
            r = requests.get(f'https://api.github.com/users/{self.username}/starred')
            if 'message' in r.json() and r.json()['message'] == 'Not Found':
                return 3
            else:
                self.collect_info(r.json())
                if len(r.json()) != 0:
                    try:
                        next_url = self.next_url_pattern.search(r.headers['Link']).group(1)
                        last_url = self.last_url_patter.search(r.headers['Link']).group(1)

                        while next_url != last_url:
                            r = requests.get(next_url)
                            next_url = self.repeated_next_url_pattern.search(r.headers['Link']).group(1)
                            self.collect_info(r.json())

                        r = requests.get(next_url)
                        self.collect_info(r.json())
                    except (IndexError, KeyError):
                        pass
                    return 0
                else:
                    return 1
        except requests.RequestException:
            return 2

    def get_result(self):
        return self.result


if __name__ == '__main__':
    codes = {1: 'This user dont have starred repos', 2: 'Connection lost', 3: 'Cannot found this user'}
    console_parser = GitApi.create_parser()
    namespace = console_parser.parse_args()
    if namespace.name:
        git_api = GitApi(namespace.name)
        result = git_api.run()
        if result != 0:
            print(codes[result])
        else:
            result = git_api.get_result()
            for result_string in result:
                print(result_string + ' : ' + str(result[result_string]))
    else:
        print('Enter username')
