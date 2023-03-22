import pytest

from automate_jw.functions.url import url_details


_TEST_URL_DETAILS = {
    "https://github.com/python/cpython/blob/main/Lib/test/test_urlparse.py": {
        "hostname": "github.com",
        "netloc": "github.com",
        "path": "/python/cpython/blob/main/Lib/test/test_urlparse.py",
        "scheme": "https",
        "url": "https://github.com/python/cpython/blob/main/Lib/test/test_urlparse.py",
    },
    "file:///tmp/url.txt": {
        "path": "/tmp/url.txt",
        "scheme": "file",
        "url": "file:///tmp/url.txt",
    },
    "sftp://user:password@203.0.113.2:22/files;user=user/logs;age=7d/?order=1#friday": {
        "fragment": "friday",
        "hostname": "203.0.113.2",
        "netloc": "user:password@203.0.113.2:22",
        "password": "password",
        "path": "/files;user=user/logs;age=7d/",
        "port": 22,
        "query": "order=1",
        "scheme": "sftp",
        "url": "sftp://user:password@203.0.113.2:22/files;user=user/logs;age=7d/?order=1#friday",
        "username": "user",
    },
    "git+ssh://git@github.com/python/cpython.git": {
        "hostname": "github.com",
        "netloc": "git@github.com",
        "path": "/python/cpython.git",
        "scheme": "git+ssh",
        "url": "git+ssh://git@github.com/python/cpython.git",
        "username": "git",
    },
    "https://GitHub.com:443/python/cpython": {
        "hostname": "github.com",
        "netloc": "GitHub.com:443",
        "path": "/python/cpython",
        "port": 443,
        "scheme": "https",
        "url": "https://GitHub.com:443/python/cpython",
    },
    "http://203.0.113.1:8000/test/": {
        "hostname": "203.0.113.1",
        "netloc": "203.0.113.1:8000",
        "path": "/test/",
        "port": 8000,
        "scheme": "http",
        "url": "http://203.0.113.1:8000/test/",
    },
    "http://[::1]:5000/test/": {
        "hostname": "::1",
        "netloc": "[::1]:5000",
        "path": "/test/",
        "port": 5000,
        "scheme": "http",
        "url": "http://[::1]:5000/test/",
    },
    "//Test": {"hostname": "test", "netloc": "Test", "url": "//Test"},
    "/Test": {"path": "/Test", "url": "/Test"},
}


@pytest.mark.parametrize(
    "url, expected_details", _TEST_URL_DETAILS.items(), ids=_TEST_URL_DETAILS.keys()
)
def test_url_details(url, expected_details):
    details = url_details(url)
    assert details == expected_details
    assert details["url"] == url
