from django.http import HttpRequest


def url_conf_change(get_response):
    def middleware(request):
        if request.user.id is not None:
            if 'group' in request.session:
                if request.session['group']['name'] == 'sch':
                    request.urlconf = 'oshstudy.url_sch'
                elif request.session['group']['name'] == 'hse':
                    request.urlconf = 'oshstudy.url_hse'
        response = get_response(request)
        return response
    return middleware
