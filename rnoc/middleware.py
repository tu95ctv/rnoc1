import pytz

from django.utils import timezone
class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname ==None:
            #tzname = 'Europe/Moscow'
            tzname = 'Asia/Bangkok'
        print 'tzname@@@@@@@@@@@@@@@',tzname, type(tzname)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()