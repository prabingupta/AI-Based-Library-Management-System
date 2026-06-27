from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import BorrowRecord, Reservation, FineRule
from members.models import Member
from books.models import BookCopy


class IssueBorrowForm(forms.ModelForm):
    member = forms.ModelChoiceField(
        queryset=Member.objects.filter(is_deleted=False, status='active'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select Member'
    )
    book_copy = forms.ModelChoiceField(
        queryset=BookCopy.objects.filter(status='available', is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select Book Copy'
    )

    class Meta:
        model = BorrowRecord
        fields = ['member', 'book_copy', 'due_date', 'notes']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_due = timezone.now() + timedelta(days=14)
        self.fields['due_date'].initial = default_due.strftime('%Y-%m-%dT%H:%M')


class ReturnBookForm(forms.Form):
    fine_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['member', 'book_copy', 'expiry_date', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'book_copy': forms.Select(attrs={'class': 'form-select'}),
            'expiry_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
