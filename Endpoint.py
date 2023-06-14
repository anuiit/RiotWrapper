'''from RequestHandler import RequestHandler

class Endpoint:
    def __init__(self, url, request_handler=None, use_platform=False, **kwargs):
        self.url = url
        self.request_handler = RequestHandler() if request_handler == None else request_handler
        self.use_platform = use_platform

    def __call__(self, **kwargs):
        # Replace placeholders in the URL with actual values from kwargs
        final_url = self.url.format(**kwargs)

        # Make the API request using request_handler and return the result
        return self.request_handler.make_request(final_url)'''
