from django.core.management import setup_environ
import mysite.settings
setup_environ(mysite.settings)

from defacements.models import Notifier, Defacements

defacements = Defacements.objects.all()[:20]

a = defacements[0]
