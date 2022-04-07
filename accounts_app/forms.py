from django import forms
from django.core import validators
from django.utils import html
from accounts_app.models import CustomUser
from tinymce.widgets import TinyMCE
from blog_app.models import Category, Tag, Article
from slider_app.models import Slider


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control d-block', 'placeholder': 'نام کاربری را وارد کنید'}),
        label='نام کاربری')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'}),
        label='رمز عبور')
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), required=False,
                                     label='مرا به خاطر بسپار')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')


class CreateNewUserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'نام کاربری را وارد کنید'}),
        label='نام کاربری',
        validators=[
            validators.MinLengthValidator(3, 'نام کاربری باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(12, 'نام کاربری باید کمتر از 12 کلمه باشد')
        ],
        required=True,
        max_length=12,
        min_length=3,
        help_text="حروف انگلیسی و اعداد حروف _،@،# مجاز است (12 کلمه مجاز میباشد)"
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'رمز عبور را وارد کنید'}),
        label='رمز عبور',
        validators=[
            validators.MinLengthValidator(12, 'رمز عبور باید  12 کلمه باشد.'),
            validators.MaxLengthValidator(12, 'رمز عبور باید 12 کلمه باشد')
        ],
        required=True,
        max_length=12,
        min_length=12,
        help_text=html.format_html(
            '<div class="help"><ul class="list-unstyled text-secondary"><li>گذرواژه شما نمی‌تواند شبیه سایر اطلاعات شخصی شما باشد.</li><li>رمز عبور شما می‌بایست حداقل از 8 حرف تشکیل شده باشد.</li><li>گذرواژه شما نمی تواند یک گذرواژه معمول باشد.</li><li>گذرواژه شما نمی تواند کلا عدد باشد</li></ul></div>')

    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'تکرار رمز عبور را وارد کنید'}),
        label='تکرار رمز عبور',
        validators=[
            validators.MinLengthValidator(12, 'تکرار رمز عبور باید  12 کلمه باشد.'),
            validators.MaxLengthValidator(12, 'تکرار رمز عبور باید  12 کلمه باشد')
        ],
        required=True,
        max_length=12,
        min_length=12,
        help_text="برای تائید، رمز عبور قبلی را وارد کنید."
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = CustomUser.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('نام کاریری قبلا ثبت شده')
        else:
            return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise forms.ValidationError('رمز عبور و تکرار آن، یکی نیستند')
        else:
            return password1


class EditUserProfileForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'first_name', 'placeholder': 'نام را وارد کنید'}),
        label='نام',
        validators=[
            validators.MinLengthValidator(3, 'نام باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(200, 'نام باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=200,
        min_length=3,
        help_text="نام کوچک خود را وارد کنید"
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'last_name', 'placeholder': 'نام خانوادگی را وارد کنید'}),
        label='نام خانوادگی',
        validators=[
            validators.MinLengthValidator(3, 'نام خانوادگی باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(200, 'نام خانوادگی باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=200,
        min_length=3,
        help_text="نام خانوادگی خود را وارد کنید"
    )

    profile_image = forms.ImageField(required=False,
                                     help_text='برای خود عکسی انتخاب کنید ( حداکثر اندازه 1 مگابایت است.(1MB) )',
                                     label='تصویر پروفایل')

    education = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'education', 'placeholder': 'تحصیلات را وارد کنید'}),
        label='تحصیلات',
        validators=[
            validators.MinLengthValidator(3, 'تحصیلات باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(200, 'تحصیلات باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=200,
        min_length=3,
        help_text="تحصیلات خود را وارد کنید"
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'آدرس کنونی را وارد کنید'}),
        label='آدرس کنونی',
        validators=[
            validators.MinLengthValidator(3, 'آدرس کنونی باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(200, 'آدرس کنونی باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=200,
        min_length=3,
        help_text="آدرس کنونی خود را وارد کنید"
    )

    about_me = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'about_me', 'placeholder': 'درباره من را وارد کنید'}),
        label='درباره من',
        validators=[
            validators.MinLengthValidator(3, 'درباره من باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(200, 'درباره من باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=200,
        min_length=3,
        help_text="درباره ی خود چیزی بنویسید"
    )

    my_skill = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'my_skill', 'placeholder': 'مهارت های من را وارد کنید'}),
        label='مهارت های من',
        validators=[
            validators.MinLengthValidator(3, 'مهارت های من باید بیشتر از 3 کلمه باشد.'),
            validators.MaxLengthValidator(500, 'مهارت های من باید کمتر از 200 کلمه باشد')
        ],
        required=False,
        max_length=500,
        min_length=1,
        help_text="مهارت های خود را بنویسید ( با , از هم جدا کنید )"
    )


class ChangeUserPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'رمز عبور را وارد کنید'}),
        label='رمز عبور',
        validators=[
            validators.MinLengthValidator(12, 'رمز عبور باید  12 کلمه باشد.'),
            validators.MaxLengthValidator(12, 'رمز عبور باید 12 کلمه باشد')
        ],
        required=True,
        max_length=12,
        min_length=12,
        help_text=html.format_html(
            '<div class="help"><ul class="list-unstyled text-secondary"><li>گذرواژه شما نمی‌تواند شبیه سایر اطلاعات شخصی شما باشد.</li><li>رمز عبور شما می‌بایست حداقل از 8 حرف تشکیل شده باشد.</li><li>گذرواژه شما نمی تواند یک گذرواژه معمول باشد.</li><li>گذرواژه شما نمی تواند کلا عدد باشد</li></ul></div>')

    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'تکرار رمز عبور را وارد کنید'}),
        label='تکرار رمز عبور',
        validators=[
            validators.MinLengthValidator(12, 'تکرار رمز عبور باید  12 کلمه باشد.'),
            validators.MaxLengthValidator(12, 'تکرار رمز عبور باید  12 کلمه باشد')
        ],
        required=True,
        max_length=12,
        min_length=12,
        help_text="برای تائید، رمز عبور قبلی را وارد کنید."
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise forms.ValidationError('رمز عبور و تکرار آن، یکی نیستند')
        else:
            return password1


class EditArticleForm(forms.Form):
    STATUS = (
        ('n', None),
        ('u', 'منتشر نشود'),
        ('w', 'درحال بررسی'),
        ('p', 'منتشر شود'),
    )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='عنوان', required=False)
    content = forms.CharField(widget=TinyMCE(attrs={'required': False, 'cols': 40, 'rows': 20}), label='محتوا',
                              required=False)
    image = forms.ImageField(label='تصویر اصلی', required=False, help_text='ابعاد 440*750')
    video_url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.aparat.com/v/MACWd'}),
        label='لینک ویدیو آپارات', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": 'custom-select mb-3'}), label='دسته بندی ها',
                                      required=False)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                         widget=forms.SelectMultiple(attrs={"class": 'custom-select mb-3'}),
                                         label='تگ ها',
                                         required=False,
                                         help_text='برای انتخاب بیش از یکی "Control"، یا "Command" روی Mac، را پایین نگه دارید.')
    status = forms.ChoiceField(choices=STATUS, label='وضعیت', widget=forms.Select(attrs={"class": 'custom-select'}),
                               required=False, initial='n')


class CategoryEditFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام دسته بندی را وارد کنید'}),
        label='نام دسته بندی',
        required=True)
    en_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام انگلیسی دسته بندی را وارد کنید'}),
        label='نام انگلیسی دسته بندی',
        required=True)


class TagEditFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام برچسب را وارد کنید'}),
        label='نام برچسب',
        required=True)
    en_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام انگلیسی برچسب را وارد کنید'}),
        label='نام انگلیسی برچسب',
        required=True)


class CreateCategoryFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام دسته بندی را وارد کنید'}),
        label='نام دسته بندی',
        required=True)
    en_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام انگلیسی دسته بندی را وارد کنید'}),
        label='نام انگلیسی دسته بندی',
        required=True)


class CreateTagFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام برچسب را وارد کنید'}),
        label='نام برچسب',
        required=True)
    en_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام انگلیسی برچسب را وارد کنید'}),
        label='نام انگلیسی برچسب',
        required=True)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['visit_count', 'date_created', 'date_update']
        widgets = {
            'creator': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tag': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

        }


class GalleryForm(forms.Form):
    image = forms.ImageField(label='تصویر')
    alt = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات تصویر'}),
                          label='توضیحات تصویر')
    article = forms.ModelChoiceField(queryset=Article.objects.all(),
                                     widget=forms.Select(attrs={"class": 'custom-select'}), label='پست')


class EditGalleryForm(forms.Form):
    image = forms.ImageField(label='تصویر')
    alt = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات تصویر'}),
                          label='توضیحات تصویر')
    article = forms.ModelChoiceField(queryset=Article.objects.all(),
                                     widget=forms.Select(attrs={"class": 'custom-select'}), label='پست')


class CreateSeoArticleListForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='عنوان', required=True)
    keywords = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='کلمات کلیدی',
                               required=True)
    description = forms.CharField(widget=TinyMCE(attrs={'required': False, 'cols': 40, 'rows': 30}), label='توضیحات',
                                  required=True)


class EditSeoArticleListForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='عنوان', required=True)
    keywords = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='کلمات کلیدی',
                               required=True)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 30}), label='توضیحات',
                                  required=True)


class EditArticleSeo(forms.Form):
    article_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(),
        label='عنوان',
        required=True
    )
    keywords = forms.CharField(
        widget=forms.TextInput(),
        label='کلید واژه ها',
        required=True,
    )
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 40, 'rows': 30}),
        label="توضیحات",
        required=True
    )


class CreateArticleSeo(forms.Form):
    article = forms.ModelChoiceField(
        queryset=Article.objects.all(),
        widget=forms.Select(attrs={'class': 'custom-select'}),
        label='انتخاب پست',
        help_text='اگر قبلا برای پستی سئو ایجاد شده، دوباره برای همان پست، سئو ایجاد نکنید'
    )
    title = forms.CharField(
        widget=forms.TextInput(),
        label='عنوان',
        required=True
    )
    keywords = forms.CharField(
        widget=forms.TextInput(),
        label='کلید واژه ها',
        required=True,
    )
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 40, 'rows': 30}),
        label="توضیحات",
        required=True
    )


class SuggestionPostForm(forms.Form):
    post = forms.ModelChoiceField(
        queryset=Article.objects.all(),
        label='پست',
        widget=forms.Select(attrs={'class': 'custom-select'}),
        help_text='اگر قبلا پستی انتخاب شده، دوباره همان پست را انتخاب نکنید'
    )


class EditCommentForm(forms.Form):
    STATUS = (
        ('n', None),
        ('a', 'قبول شود'),
        ('r', 'رد شود'),
    )
    post = forms.ModelChoiceField(
        queryset=Article.objects.all(),
        label='پست',
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام و نام خانوادگی',
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='ایمیل',
        required=True
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='نظر',
        required=True
    )
    status = forms.ChoiceField(choices=STATUS, label='وضعیت', widget=forms.Select(attrs={"class": 'custom-select'}),
                               required=False, initial='n')


class SliderForm(forms.Form):
    STATUS = (
        ('u', 'منتشر نشود'),
        ('p', 'منتشر شود'),
    )
    title = forms.CharField(
        widget=TinyMCE(attrs={'required': False, 'cols': 40, 'rows': 20}),
        label='عنوان'
    )
    image = forms.ImageField(required=False)
    url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS, label='وضعیت', widget=forms.Select(attrs={"class": 'custom-select'}),
                               required=False, initial='u')
    slider_id = forms.IntegerField(widget=forms.HiddenInput())


class CreateSliderFrom(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
