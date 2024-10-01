from django.test import TestCase
from .forms import FarmerSignUpForm, CoordinatorSignUpForm

class SignUpFormTest(TestCase):
    def test_valid_farmer_signup(self):
        form_data = {
            'username': 'farmer_test',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'farmer@example.com',
        }
        form = FarmerSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.profile.user_type, 'Farmer')

    def test_valid_coordinator_signup(self):
        form_data = {
            'username': 'coordinator_test',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'coordinator@example.com',
        }
        form = CoordinatorSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.profile.user_type, 'Coordinator')
