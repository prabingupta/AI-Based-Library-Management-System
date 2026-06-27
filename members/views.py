from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Member
from .forms import MemberForm, MemberUserForm

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class MemberListView(View):
    template_name = 'members/list.html'

    def get(self, request):
        members = Member.objects.filter(is_deleted=False).select_related('user')
        query = request.GET.get('q', '')
        membership_type = request.GET.get('type', '')
        status = request.GET.get('status', '')

        if query:
            members = members.filter(
                Q(card_number__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__email__icontains=query)
            )

        if membership_type:
            members = members.filter(membership_type=membership_type)

        if status:
            members = members.filter(status=status)

        context = {
            'members': members,
            'query': query,
            'selected_type': membership_type,
            'selected_status': status,
            'total_count': members.count(),
            'page_title': 'Members',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MemberDetailView(View):
    template_name = 'members/detail.html'

    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk, is_deleted=False)
        borrow_history = member.borrowings.select_related(
            'book_copy__book'
        ).order_by('-borrow_date')[:10]
        context = {
            'member': member,
            'borrow_history': borrow_history,
            'page_title': member.user.get_full_name(),
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MemberCreateView(View):
    template_name = 'members/form.html'

    def get(self, request):
        user_form = MemberUserForm()
        member_form = MemberForm()
        context = {
            'user_form': user_form,
            'member_form': member_form,
            'page_title': 'Add Member',
            'action': 'Add',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = MemberUserForm(request.POST)
        member_form = MemberForm(request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            messages.success(request, f'Member "{user.get_full_name()}" added successfully.')
            return redirect('members:detail', pk=member.pk)
        context = {
            'user_form': user_form,
            'member_form': member_form,
            'page_title': 'Add Member',
            'action': 'Add',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MemberEditView(View):
    template_name = 'members/form.html'

    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk, is_deleted=False)
        user_form = MemberUserForm(instance=member.user)
        member_form = MemberForm(instance=member)
        context = {
            'user_form': user_form,
            'member_form': member_form,
            'member': member,
            'page_title': 'Edit Member',
            'action': 'Update',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        member = get_object_or_404(Member, pk=pk, is_deleted=False)
        user_form = MemberUserForm(request.POST, instance=member.user)
        member_form = MemberForm(request.POST, instance=member)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            member_form.save()
            messages.success(request, f'Member "{user.get_full_name()}" updated successfully.')
            return redirect('members:detail', pk=member.pk)
        context = {
            'user_form': user_form,
            'member_form': member_form,
            'member': member,
            'page_title': 'Edit Member',
            'action': 'Update',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MemberDeleteView(View):
    def post(self, request, pk):
        member = get_object_or_404(Member, pk=pk, is_deleted=False)
        name = member.user.get_full_name()
        member.is_deleted = True
        member.save()
        messages.success(request, f'Member "{name}" has been removed.')
        return redirect('members:list')
