class SomeClient(object):
    """
    The client used to make calls to the backend site. Should take care of the authentication
    against the server, error handling, logging in Sentry (regular logger), and returning
    the response data.
    """
    allowed_methods = ['get', 'post', 'patch', 'put', 'delete', 'head', ]

    def __init__(self, request=None):
        if not request:
            self.token = ''
            return

        if hasattr(request, 'token'):
            self.token = request.token
        else:
            self.token = ''

    def validate_method(self, method):
        if method not in self.allowed_methods:
            raise ApiException("Method {} not allowed.".format(method.upper()))

    def create_credentials(self):
        return (
            settings.SB_API_USER,
            settings.SB_API_PW
        )

    def create_headers(self):

        headers = {'Accept': 'application/json'}
        # if settings.DEBUG is True:
        #     headers['Authorization'] = 'Token {}'.format(settings.USER_1_TOKEN)

        if self.token:
            headers['Authorization'] = 'Token {}'.format(self.token)

        return headers

    def build_api_url(self, endpoint):
        return "{}://{}{}".format(
            settings.SB_API_HTTP_PROTOCOL,
            settings.SB_API_HOST,
            endpoint,
        )

    def send_request(self, url, method, data, files=None):
        http_method = getattr(requests, method)

        response = http_method(
            url=self.build_api_url(url),
            json=data,
            headers=self.create_headers(),
            files=files
        )
        response.encoding = 'UTF-8'
        if response.status_code >= 500:
            raise Http500("API error API status: {} DETAIL: {}".format(
                response.status_code,
                response.text
            ))

        return response

    def handle_response(self, response, raise_404):
        """ What should this method do apart from 404 """
        if raise_404 and response.status_code == 404:
            raise Http404()
        if response.status_code > 400 and response.status_code != 404:
            raise ApiException("Invalid result. Status code: {}. {}".format(
                response.status_code, response.text[:255]
            ))

    def _api_call(self, url, attr, raise_404, method, data, files=None):
        """ Real API call method, hidden from outside so the logging wrapper is used """
        self.validate_method(method)

        response = self.send_request(url, method, data, files=files)
        self.handle_response(response, raise_404=raise_404)

        # Only return content if it actually has content
        if not response.ok or response.status_code == 204:
            return {'status': response.status_code, 'detail': response.text}

        # Allow requesting a specific attribute
        if attr:
            return response.json()[attr]

        return response.json()

    def api_call(self, url, attr=None, raise_404=True, method='get', data=None, files=None):
        """ Wrapper around the possible errors of the API, logging them whenever necessary """
        try:
            return self._api_call(
                url=url,
                attr=attr,
                raise_404=raise_404,
                method=method,
                data=data,
                files=files
            )

        except Http404:
            raise

        except ApiException as exc:
            logger.exception(
                "Exception occurred in the API client. \
                The details of the error are '{}'.".format(str(exc))
            )
            return None

        except Http500 as exc:
            logger.exception(
                "Exception occurred in the Schoolbank API. \
                The details of the error are '{}'.".format(str(exc))
            )
            raise

        except Exception as request_exc:
            logger.exception(
                "Exception '{}' occurred on the API request. \
                The details for the error are '{}'.".format(request_exc.__class__.__name__,
                                                            str(request_exc))
            )
            return None


class NewsFeedClient(SomeClient):

    def get_news(self, count=10, offset=0):
        data = self.api_call(
            '/v1/news_feed?count={}&offset={}'.format(count, offset)
        )
        return data


class MemoryClientService(SomeClient):

    def update_memory(self, memory_id, data):
        data['school_slug'] = data.pop('school')
        return self.api_call(
            url='/v1/memories/{}/'.format(memory_id),
            data=data,
            method='put',
        )

    def delete_memory(self, memory_id):
        return self.api_call(
            url='/v1/memories/{}/'.format(memory_id),
            method='delete',
        )

    def add_memory(self, data):
        data['school_slug'] = data['school']
        return self.api_call(
            url='/v1/memories/',
            data=data,
            method='post'
        )

    def add_reaction(self, data):
        return self.api_call(
            url='/v1/reactions/',
            data=data,
            method='post'
        )

