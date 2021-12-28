from django import forms


class CustomSelectWidget(forms.Select):
    template_name = 'store/tst.html'


class SizeForm(forms.Form):

    '''in the single_product view, we pass the product instance to the form.'''
    def __init__(self, instance, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)
        self.instance = instance
        
        '''self.instance.sizes.all() gives a "<QuerySet [<Size: S>, <Size: M>]>" for example.
        We split by ": " and get the 0 - indexed value, which is the size letter.
        We cast it to str before splitting since it's a 'Size' object. 
        This leaves us with a "['S', 'M']" for example.'''
        list_of_instance_sizes = [str(size).split(": ")[0] for size in self.instance.sizes.all()]

        '''We double the size in a list of tuples, because that's what django choices require.'''
        final_choices = [(choice, choice) for choice in list_of_instance_sizes]
        
        '''We add a "size" field via self.fields[...], because we can't do it from outside the 
        __init__. At least I couldn't find a way.'''
        self.fields['size'] = forms.ChoiceField(
            # widget=CustomSelectWidget(
            #     attrs={'class': 'btn btn-primary'}), 
            choices=final_choices)

