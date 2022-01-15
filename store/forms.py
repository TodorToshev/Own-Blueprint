from django import forms
from .models import Order, ProductReview

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CustomSelectWidget(forms.Select):
    template_name = 'store/tst.html'


class OrderForm(forms.Form):

    '''in the single_product view, we pass the product instance to the form.'''
    def __init__(self, instance, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.instance = instance
        
        self.fields['size'] = forms.ModelChoiceField(
            queryset=self.instance.sizes.all(),
            widget=forms.RadioSelect())
        
        self.fields['quantity'] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), initial=1)

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        #remove help text from form fields
        for field in self.fields:
            self.fields[field].label = ''

    class Meta:
        model = ProductReview
        fields = ['name', 'email', 'comment',]
        widgets = {'name': forms.widgets.TextInput(attrs={
                   'placeholder': 'Name'}),
                'email': forms.widgets.TextInput(attrs={
                    "placeholder": 'Email'}),
                'comment': forms.widgets.Textarea(attrs={
                    "placeholder": 'Review', "rows": "5"}),
               }


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'country', 'city', 'address', 'postal_code']