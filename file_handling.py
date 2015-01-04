import hashlib
import os
import urllib2


def check_md5(file_path, target_md5):
    file_md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    return file_md5 == target_md5


def download(source_url, dest_file_path):
    d = urllib2.urlopen(source_url)
    output = open(dest_file_path, 'wb')
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
            print('{f} already exists - No MD5 checksum given - assuming file is OK and skipping MD5 check.'.format(
                f=dest_filename))
            return dest_file_path
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