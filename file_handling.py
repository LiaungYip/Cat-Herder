import hashlib
import os
import urllib2


def check_md5(file_path, target_md5):
    file_md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    return file_md5 == target_md5


def download(source_url, dest_file_path):
    try:
        d = urllib2.urlopen(source_url)
    except urllib2.HTTPError, e:
        if e.code == 404:
            print ("ERROR - {u} was 404. Check the exact spelling of the pack name and pack version.".format(u=source_url))
            quit()
    # urllib doesn't always seem to throw a HTTPError in the case of a 404. Seems quite happy to open
    # a HTML 'Sorry, 404' page if the server presents one. Hence this additional check.
    if d.getcode() == 404:
        print ("ERROR - {u} was 404. Check the exact spelling of the pack name and pack version.".format(u=source_url))
        quit()
    # Getting 'text/html' usually indicates something is buggered.
    # i.e. NodeCDN gives a 404 html page but no 404 response code.
    if d.headers.getheaders('Content-Type')[0] == 'text/html':
        print ("""ERROR - requested {u}.
However! server responded with Content-Type 'text/html' instead of an actual file.
Maybe a 404 page?. Check the exact spelling of the pack name and pack version.""".format(u=source_url))
        quit()
    with open(dest_file_path, 'wb') as output:
        output.write(d.read())
        output.close()


def fetch_url(source_url, dest_filename, md5=None):
    """
    Fetch the file from source_url, save it to the current working directory, and check MD5.
    If the file is already downloaded to cache, check its MD5.
    """
    dest_file_path = dest_filename

    if os.path.isfile(dest_file_path):
        if md5 is None:
            print('{f} already exists - No MD5 checksum given - redownloading file.'.format(
                f=dest_filename))
            # return dest_file_path
            os.remove(dest_file_path)
        elif check_md5(dest_file_path, md5):
            print('{fn} already exists - MD5 of cached file matches {m} - Using cached copy of {fn}'.format(m=md5,
                                                                                                            fn=dest_file_path))
            return dest_file_path
        else:
            print('Cached copy of {fn} failed MD5 check.'.format(fn=dest_file_path))
            os.remove(dest_file_path)

    print('Downloading new copy of {fn} from {url}'.format(fn=dest_file_path, url=source_url))
    download(source_url, dest_file_path)
    return dest_file_path


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)