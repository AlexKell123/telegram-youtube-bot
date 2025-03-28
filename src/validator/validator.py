import re

class Validator:
    def __init__(self):
        self.youtube_regex = (r'(https?://)?(www\.)?'
                               '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                               '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    def url_to_valid(self, url):
        youtube_regex_match = re.match(self.youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match.group(6)
        else:
            raise Exception('NOT_VALID_URL')
