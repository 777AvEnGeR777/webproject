from django import forms
from ask.models import Question, Tag, Profile, Answer
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(label="Login:", max_length=30)
    password = forms.CharField(label="Password:", widget=forms.PasswordInput())


class SignupForm(forms.Form):
    login = forms.CharField(label="Login:", max_length=30)
    email = forms.EmailField(label="E-mail:")
    nickname = forms.CharField(label="Nickname:", max_length=30)
    password = forms.CharField(label="Password:", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm password:", widget=forms.PasswordInput())
    avatar = forms.ImageField(label="Upload avatar:", required=False)

    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            User.objects.get_by_natural_key(login)
        except User.DoesNotExist:
            return login
        raise forms.ValidationError("This user is already exists!")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
           User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("This email is already registered!")

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            User.objects.get(first_name=nickname)
        except User.DoesNotExist:
            return nickname
        raise forms.ValidationError("This nickname is already taken!")

    def clean_confirm_password(self):
        passwd = self.cleaned_data['password']
        confirm_passwd = self.cleaned_data['confirm_password']
        if not confirm_passwd:
            raise forms.ValidationError("Please, confirm your password!")
        if passwd != confirm_passwd:
            raise forms.ValidationError("Passwords doesn't match!")

    def save(self):
        user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'],
                                        self.cleaned_data['password'], first_name=self.cleaned_data['nickname'])
        profile = Profile.objects.create(user=user)
        print self.cleaned_data
        if self.cleaned_data['avatar'] is not None:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()
        return profile


class SettingsForm(forms.Form):
    login = forms.CharField(label="Login:", max_length=30, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(label="E-mail:")
    nickname = forms.CharField(label="Nickname:", max_length=30)
    avatar = forms.ImageField(label="Upload avatar:", required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        user = User.objects.get_by_natural_key(self.cleaned_data['login'])
        if user.email != email:
            raise forms.ValidationError("This email is already registered!")
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            User.objects.get(first_name=nickname)
        except User.DoesNotExist:
            return nickname
        user = User.objects.get_by_natural_key(self.cleaned_data['login'])
        print nickname
        print user.first_name
        if user.first_name != nickname:
            raise forms.ValidationError("This nickname is already taken!")
        return nickname

    def save(self):
        login = self.cleaned_data['login']
        email = self.cleaned_data['email']
        nick = self.cleaned_data['nickname']
        avatar = self.cleaned_data['avatar']
        user = User.objects.get_by_natural_key(login)
        profile = Profile.objects.get(user=user)
        user.email = email
        user.first_name = nick
        user.save()
        print self.cleaned_data
        if avatar is not None:
            profile.avatar = avatar
            profile.save()


class QuestionForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=75)
    text = forms.CharField(widget=forms.Textarea(), max_length= 5000)
    tag_names = forms.CharField(label="Tags:", max_length=75,
                                widget=forms.TextInput(attrs={'placeholder': 'Tags separated by space'}))
    tags = []

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean_tags_names(self):
        tag_names = self.cleaned_data['tag_names']
        print tag_names
        for tag_name in tag_names.split(' '):
            tag, flag = Tag.objects.get_or_create(name=tag_name)
            self.tags.append(tag)

    def save(self):
        self.cleaned_data['author'] = Profile.objects.get(user=self._user)
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'],
                            author=self.cleaned_data['author'])
        question.save()
        for tag in self.tags:
            question.tags.add(tag)
        question.save()
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'answer',
                'rows': 5,
                'maxlength': 5000,
                'placeholder': 'Enter your answer here...'
            })
        }

