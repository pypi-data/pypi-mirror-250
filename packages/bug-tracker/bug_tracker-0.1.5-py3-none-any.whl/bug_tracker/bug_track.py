import traceback
import sys

class ConsoleExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, e)
            raise
        return response

    def process_exception(self, request, exception):
        exc_info = sys.exc_info()
        
        print("-" * 30 + "Exception" + "-" * 50)
        print('\n'.join(traceback.format_exception(*(exc_info or sys.exc_info()))))
        print("-" * 88)
        value = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        import requests

        url = "https://productivity.colanapps.in/api/bugtrack/"

        payload = {'test': value}

        headers = {
        'Authorization': 'Bearer afe699004333ed37265b189677746d11a9463ab9'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
