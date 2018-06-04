from datetime import datetime

from django.contrib.auth.models import User
from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		users = User.objects.filter(is_superuser=True).order_by('id')
		users.filter(last_name='ma')

		return {
			'now': datetime.now(),
			'users': users
		}
