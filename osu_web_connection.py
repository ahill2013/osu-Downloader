import os
import sys

import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote


def convert_to_valid_filename(filename):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in valid_chars else '_' for c in filename)


class OsuWebConnection:
    # old site
    # login_url = "https://osu.ppy.sh/forum/ucp.php?mode=login"
    # New site
    home_url = "https://osu.ppy.sh/home"
    login_url = "https://osu.ppy.sh/session"

    def __init__(self):
        self.session = requests.Session()
        print("Login:")
        self.login = input()
        print("Password:")
        self.password = input()
        self.token = ""
        self.initial_connection()
        self.do_login()

    def initial_connection(self):
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})
        self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        self.session.headers.update({'Accept-Language': 'en-US,en;q=0.5'})
        self.session.headers.update({'Accept-Encoding': 'gzip, deflate'})
        self.session.headers.update({'Connection': 'keep-alive'})

        r = self.session.get(self.home_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.token = soup.find('input').attrs['value']

        print("Session token: " + self.token)

    def do_login(self):
        print("Logging in osu! site with user " + self.login + "....")
        r = self.session.post(OsuWebConnection.login_url,
                              data={'_token': self.token,
                                    'username': self.login,
                                    'password': self.password})
        # print(r.headers)

    """def is_logged(self):
        r = self.session.get(OsuWebConnection.login_url)
        text = r.text
        # print(text)
        if "Username:" in text and "Password:" in text and \
                "Log me on automatically each visit" in text and \
                "Hide my online status this session" in text:
            return False
        elif "Announcements (click for more)" in text:
            return True
        return False
    """

    def download_sync(self, beatmap_id, base_path):
        # if not self.is_logged():
        #     self.do_login()

        # beatmap_url = "https://osu.ppy.sh/d/" + beatmap_id
        # r = self.session.get(beatmap_url, stream=True)

        beatmap_url = "https://osu.ppy.sh/beatmapsets/" + beatmap_id + '/download'
        r = self.session.get(beatmap_url, allow_redirects=False)

        # if r.headers['Content-Type'] != "application/download":
        if 'Page Missing' in r.text:
            # beatmap not available
            # beatmap.download_status = "NOT AVAILABLE"
            sys.stdout.write("Beatmap " + str(beatmap_id) + " not available.")
            sys.stdout.flush()
            return -1

        soup = BeautifulSoup(r.text, 'html.parser')
        href = soup.find('a')
        name = unquote(href.text).split("fs=", 2)[1].split(".osz", 2)[0]

        filename_base = convert_to_valid_filename(name)
        filename_temp = filename_base + ".temp"
        filename_final = filename_base + ".osz"
        # beatmap available, download it
        # print(r.text)
        url = r.headers['location']
        print("True Download URL: " + url)
        r = self.session.get(url, stream=True)
        filesize = int(r.headers['Content-Length']) / 1024.0 / 1024.0
        print("Downloading '" + filename_final + "' (%.2f MB)..." % filesize)
        with open(base_path + "/" + filename_temp, 'wb') as f:
            counter = -1
            for chunk in r.iter_content(chunk_size=1023):
                if chunk:
                    f.write(chunk)
                    counter += 1023
                    percent_done = counter / int(r.headers['Content-Length']) * 100
                    # print("%d %f%%\n" % (counter, percent_done))
                    sys.stdout.write("\r [%-20s] %d%%  (%.2fMB/%.2fMB)" %
                                     ('='*int(percent_done/5), int(percent_done), counter / 1024 / 1024, filesize))
                    sys.stdout.flush()
        os.rename(base_path + "/" + filename_temp, base_path + "/" + filename_final)
        sys.stdout.write("\nFinished download of '" + filename_final + "'")
        sys.stdout.flush()
        # beatmap.download_status = "DOWNLOADED"
        return 0

    def close(self):
        self.session.close()
