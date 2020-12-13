from django import forms
from .models import Comment

# форма для отправки писем
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# форма для отправки и валидации комментариев
class CommentForm(forms.ModelForm):
    # Все, что нужно для создания формы из модели, –указать, какую модель 
    # использовать в опциях класса Meta. Django найдет нужную модель и 
    # автоматически построит форму. Каждое поле модели будет сопоставлено полю 
    # формы соответствующего типа. По умолчанию Django использует все поля 
    # модели.Но мы можем явно указать, какие использовать, а какие – нет. Для 
    # этого достаточно определить списки fields или exclude соответственно. 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# Обработчик поиска
class SearchForm(forms.Form):
    query = forms.CharField()
