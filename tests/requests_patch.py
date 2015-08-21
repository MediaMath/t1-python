import requests

def patched_extract_cookies_to_jar(jar, request, response):
    """Patched version to support mocked HTTPResponses from Responses.

    :param jar: cookielib.CookieJar (not necessarily a RequestsCookieJar)
    :param request: our own requests.Request object
    :param response: urllib3.HTTPResponse object
    """
    if not (hasattr(response, '_original_response') and
                response._original_response):
        # just grab the headers from the mocked response object
        res = requests.cookies.MockResponse(response.headers)
    else:
        # the _original_response field is the wrapped httplib.HTTPResponse object
        # pull out the HTTPMessage with the headers and put it in the mock:
        res = requests.cookies.MockResponse(response._original_response.msg)

    req = requests.cookies.MockRequest(request)
    jar.extract_cookies(res, req)

