from django import forms
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()


class MemberUserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep current'}),
        help_text='Only fill this when creating a new member.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'role', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'card_number', 'membership_type', 'status',
            'membership_start', 'membership_end',
            'max_books_allowed', 'address', 'emergency_contact', 'notes',
        ]
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'membership_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'membership_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_books_allowed': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
