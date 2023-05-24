from django.forms import Form, CharField


class OrderForm(Form):
    salon = CharField(max_length=50)
    master = CharField(max_length=50)
    service = CharField(max_length=50)