from django.test import TestCase

from candidates.models import Candidate


class CandidateModelTest(TestCase):
    def setUp(self):
        # Set up a candidate for testing
        self.candidate = Candidate.objects.create(
            name="Ajay Kumar Yadav",
            age=25,
            gender="Male",
            email="ajay@example.com",
            phone_number="1234567890",
        )

    def test_candidate_creation(self):
        # Test candidate creation
        self.assertEqual(self.candidate.name, "Ajay Kumar Yadav")
        self.assertEqual(self.candidate.age, 25)
        self.assertEqual(self.candidate.gender, "Male")
        self.assertEqual(self.candidate.email, "ajay@example.com")
        self.assertEqual(self.candidate.phone_number, "1234567890")

    def test_candidate_str(self):
        # Test string representation of the Candidate
        self.assertEqual(str(self.candidate), "Ajay Kumar Yadav")
