**Synopsis**

For this project, you’ll build a form that takes in details about a registered user and displays those details on a profile page. The profile page should only be visible once the user has logged in.The profile page should include first name, last name, email, date of birth, confirm email, short bio and the option to upload an avatar.

You’ll also set up validation for email, date of birth and the biography. The Date of Birth validation should accept three date formats: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. The Email validation should check if the email addresses match and are in a valid format. The bio validation should check that the bio is 10 characters or longer and properly escapes HTML formatting.

You’ll also create a "change password page" that updates the user’s password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy:


**Code Example**

The key to making this project successful was the extension of the built in user model to a profile model

    class Profile(models.Model):
        username = models.OneToOneField(User, on_delete=models.CASCADE)
        DOB = models.DateField(null=True, blank=True)
        bio = models.TextField(validators=[min_length_validator])
        avatar = models.ImageField(upload_to='avatars/')
    
        def __str__(self):
            return str(self.username)

Incorporating custom validators was also a key step

    class SpecialCharactersPasswordValidator(object):
        """Validator checks to see if a special
        character exists per the list below"""
        def validate(self, password, user=None):
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if not any(char in special_characters for char in password):
                raise ValidationError(_('Password must contain '
                                        'at least on special character'))
    
        def get_help_text(self):
            return "Your password must contain " \
                   "at least on special character."

**Motivation**

The motivation of this project was to use the Django framework to build a series of forms, while extending the out of the box Django model to include additional data elements to build out a user profile.

**Installation**

To install the project download all files to a location of your choosing on your computer, log into the terminal (on a MAC) and instantiate the program from the directory where you stored the files as follows:

	1) Unzip the images folder in the static directory
	2) Ensure Django is installed: pip3 install django
	3) Start new Django Project: django-admin startproject project_7
	4) Start new Django App in the project directory: python3 manage.py startapp accounts
	6) Migrate models.py to accounts project: python3 manage.py migrate
	7) Finalize migrations to minerals project: python3 manage.py makemigrations
	8) Run local environment on port 8000: python3 manage.py runserver 0.0.0.0:8000

**Tests**

n/a

**Contributors**

This project was inspired by the teachers at teamtreehouse.com and was developed by Taylor.

**License**

Opensource for your enjoyment!