from django import forms


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
        
        self.fields['quantity'] = forms.IntegerField()

