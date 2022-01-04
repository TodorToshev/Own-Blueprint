from django import forms
from .models import ProductComment

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

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        
        #remove help text from form fields
        for field in self.fields:
            self.fields[field].label = ''

    class Meta:
        model = ProductComment
        fields = ['name', 'email', 'comment',]
        widgets = {'name': forms.widgets.TextInput(attrs={
                   'placeholder': 'Name'}),
                'email': forms.widgets.TextInput(attrs={
                    "placeholder": 'Email'}),
                'comment': forms.widgets.Textarea(attrs={
                    "placeholder": 'Review', "rows": "5"}),
               }
