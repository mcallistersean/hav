from django.conf import settings

import base64
import hashlib
import hmac
import textwrap

imgproxy_key = bytes.fromhex(settings.IMAGEPROXY_KEY)
imgproxy_salt = bytes.fromhex(settings.IMAGEPROXY_SALT)

defaults = {
    "resize": "fill",
    "width": 300,
    "height": 300,
    "gravity": "no",
    "enlarge": 1,
    "extension": "png",
}


def generate_imgproxy_url(url, **kwargs):
    encoded_url = base64.urlsafe_b64encode(url).rstrip(b"=").decode()
    # You can trim padding spaces to get good-looking url
    encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))

    url_kwargs = dict(
        defaults,
        **kwargs,
        encoded_url=encoded_url
    )

    path = "/{resize}/{width}/{height}/{gravity}/{enlarge}/{encoded_url}.{extension}".format(**url_kwargs).encode()

    digest = hmac.new(imgproxy_key, msg=imgproxy_salt + path, digestmod=hashlib.sha256).digest()

    protection = base64.urlsafe_b64encode(digest).rstrip(b"=")
    url = b'http://127.0.0.1:8088/%s%s' % (
        protection,
        path,
    )

    return url.decode()