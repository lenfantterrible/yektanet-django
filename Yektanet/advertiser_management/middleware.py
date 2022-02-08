
def filter_ip_middleware(get_response):

    def middleware(request):

        if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        request.ip = ip
        response = get_response(request)

        return response

    return middleware