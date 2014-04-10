from django.forms import CharField, Textarea, Form

class searchForm(Form):
    search_data = CharField(required=True, widget=Textarea)

    def send(self):
        search_data = self.cleaned_data['search_data']