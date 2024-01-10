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
