import json
import os
import re
import requests
import sys

# Shamelessly inspired from git-pw
def download_file(url, directory, filename=None):
    response = requests.get(url);

    if not filename:
        header = re.search('filename=(.+)',
                           response.headers.get('content-disposition') or '')
        if not header:
            raise ValueError("Unexpeted: Download {} has no filename".format(url))
        filename = header.group(1)

    outpath = os.path.join(directory, filename)

    with open(outpath, 'wb') as f:
        # we use iter_content because patches can be binary
        for block in response.iter_content(1024):
            f.write(block)

    return outpath

def dump_this_json(f):
    def decorate_json_dumps(*args,**kwargs):
        j = f(*args,**kwargs)
        return json.dumps(j, indent = 2)
    return decorate_json_dumps

class PWResource:
    """ Concourse patchwork resource implementation """

    def get_pw(self, url, params):
        r = requests.get(url, params)
        if r.status_code != 200:
            raise ConnectionError("Failed to get url {}".format(url))
        return r

    def __init__(self, data: dict):
        self.data = json.loads(data)
        source = self.data["source"];
        self.url = "/".join((source["uri"], "api/1.1", ""))
        self.params = [('project', source["project"])]
        self.get_pw(self.url, self.params)

    @dump_this_json
    def cmd_check(self, version=None):
        version = self.data.get("version")
        url = self.url + "series/"
        params = [('order', '-id')] + self.params
        r = self.get_pw(url, params)
        series = r.json()

        results = []
        for s in series:
            results.insert(0, {"ref": str(s["id"])})
            if (version is None) or s["id"] == int(version["ref"]):
                # Got the matching version, stop here
                return results

        # Uh-oh: We did not find the version - assume it does not exist
        # TODO: handle pagination
        return [results[-1]]

    in_metadata_keys = [ 'url', 'web_url', 'name', 'date', 'mbox' ]

    @dump_this_json
    def cmd_in(self, in_dir):
        version = self.data["version"]
        url = self.url + "series/" + version["ref"] + "/"
        r = self.get_pw(url, self.params)
        series = r.json()
        download_file(series['mbox'], in_dir, "mbox.patch")

        # We are nice - so download each patches
        single_dir = os.path.join(in_dir, "single")
        os.mkdir(single_dir)
        patches = series["patches"]
        for patch in patches:
            download_file(patch['mbox'], single_dir)

        # Copy some data over
        metadata = list()
        for k in PWResource.in_metadata_keys:
            metadata.append({k : series[k]})

        result = dict()
        result["version"] = version
        result["metadata"] = metadata
        return result

