from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class UserCustomCreationForm(UserCreationForm):
	
	email = forms.EmailField(
		label ="이메일",
		required=True,
		help_text='example@example.com 의 형식으로 입력해주세요',
		error_messages={
			'required':'이메일을 입력해주세요',
			'invalid':'이메일 형식이 잘못되었습니다.',
		},
		max_length=30,
		widget=forms.EmailInput(
			attrs={
				'class': 'form-control mb-2',
				'placeholder': '이메일을 입력해주세요',
			}
		),
	)

	username = forms.CharField(
		label = "닉네임",
		required = True,
		help_text='최대 20 자까지 입력 가능합니다',
		error_messages={
			'required' : '닉네임을 입력해주세요',
			'invalid' : '닉네임 형식이 잘못되었습니다',
		},
		max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control mb-2',
				'placeholder':'닉네임을 입력해주세요',
			}
		),
	)

	password1 = forms.CharField(
		label = "비밀번호",
		required = True,
		help_text='최소한 8 글자, 최대 20글자까지 설정가능합니다',
		max_length=20,
		min_length=8,
		error_messages={
			'required':'비밀번호를 입력해주세요',
			'max_length':'비밀번호 글자 수가 20을 초과하셨습니다',
			'min_length':'비밀번호는 최소한 8 글자 이상 입력해주세요',
		},
		widget=forms.PasswordInput(
			attrs={
				'placeholder':'비밀번호를 입력해주세요',
				'class':'form-control mb-2',
			}
		),
	)
	
	password2 = forms.CharField(
		label = "비밀번호 확인",
		required = True,
		max_length=20,
		min_length=8,
		error_messages={
			'required':'비밀번호를 재확인해주세요',
		},
		widget=forms.PasswordInput(
			attrs={
				'placeholder':'비밀번호를 다시 입력해주세요',
				'class':'form-control mb-2',
			}
		),
	)
	
	first_name = forms.CharField(
		label = "이름",
		required = False,
		help_text='필수사항이 아닙니다',
		max_length = 20,
		min_length = 1,
		widget=forms.TextInput(
			attrs={
				'placeholder':'이름을 입력해주세요',
				'class':'form-control mb-2',
			}
		),
	)
	last_name = forms.CharField(
		label = "성",
		required = False,
		max_length = 20,
		min_length = 1,
		help_text='필수사항이 아닙니다',
		widget=forms.TextInput(
			attrs={
				'placeholder':'성을 입력해주세요',
				'class':'form-control mb-2',
			}
		),
	)
	
	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
				raise  ValidationError("이미 존재하는 닉네임입니다")
		return username
	
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			raise ValidationError("이미 존재하는 이메일입니다")
		return email
	
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		
		if password1 and password1 and password1 != password2:
			raise ValidationError("비밀번호를 다시 확인해주세요")
		
		return password2
	
	# def save(self, commit=True):
	# 	user = User.objects.create_user(
	# 		self.cleaned_data['username'],
	# 		self.cleaned_data['email'],
	# 		self.cleaned_data['password1'],
	# 		self.cleaned_data['first_name'],
	# 		self.cleaned_data['last_name'],
	# 	)
	
	class Meta:
		model = get_user_model()
		fields = ('email', 'username', 'first_name', 'last_name',)