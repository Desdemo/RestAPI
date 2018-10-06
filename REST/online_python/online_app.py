import subprocess
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.conf.urls import url, re_path
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


setting = {
    'DEBUG': True,
    'ROOT_URLCONF': __name__

}
settings.configure(**setting)


def home(request):
    with open('index.html', 'rb') as f:
        html = f.read()
        return HttpResponse(html)


def run_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code],
                                         universal_newlines=True,
                                         stderr=subprocess.STDOUT,
                                         timeout=30)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time OUT !!!', e.output])
    return output


@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse(data={'output': output})


urlpatterns = [url('^$', home, name='home'),
               url('^api/$', api, name='api')]


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
