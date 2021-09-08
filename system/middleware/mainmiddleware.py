from django.contrib.auth.models import User, Group


def group(get_response):
    def middleware(request):
        if request.user.id is not None:
            if 'group' not in request.session:
                group_name = User.objects.get(id=request.user.id).groups.all().values()
                for gr in group_name:
                    request.session['group'] = gr
        response = get_response(request)
        return response
    return middleware
