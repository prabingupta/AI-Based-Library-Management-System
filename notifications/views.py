from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from .models import Notification


@method_decorator(login_required, name='dispatch')
class NotificationListView(View):
    template_name = 'notifications/list.html'

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        filter_type = request.GET.get('type', '')
        if filter_type == 'unread':
            notifications = notifications.filter(is_read=False)
        elif filter_type == 'read':
            notifications = notifications.filter(is_read=True)

        unread_count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()

        context = {
            'notifications': notifications,
            'unread_count': unread_count,
            'filter_type': filter_type,
            'total_count': notifications.count(),
            'page_title': 'Notifications',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MarkReadView(View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.status = 'read'
        notification.save()
        return JsonResponse({'status': 'ok'})


@method_decorator(login_required, name='dispatch')
class MarkAllReadView(View):
    def post(self, request):
        Notification.objects.filter(
            user=request.user, is_read=False
        ).update(is_read=True, read_at=timezone.now(), status='read')
        return JsonResponse({'status': 'ok'})
