from django.http import HttpRequest
from company.models import Company


def select_activated_user_company(get_response):
    def middleware(request):
        if request.user.id is not None:
            if 'company_id' not in request.session:
                if request.session['group']['name'] == 'sch' or request.session['group']['name'] == 'hse':
                    company_id = Company.objects.get(user_id=request.user.id, activated=1)
                    request.session['company_id'] = company_id.id
                else:
                    request.session['company_id'] = None
        response = get_response(request)
        return response
    return middleware
