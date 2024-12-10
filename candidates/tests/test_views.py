from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from candidates.models import Candidate


class CandidateViewSetTest(APITestCase):
    def setUp(self):
        # Create candidate objects for testing
        self.candidate1 = Candidate.objects.create(
            name="Ajay Kumar Yadav",
            age=25,
            gender="Male",
            email="ajay@example.com",
            phone_number="1234567890",
        )
        self.candidate2 = Candidate.objects.create(
            name="Ramesh Kumar Yadav",
            age=30,
            gender="Male",
            email="ramesh@example.com",
            phone_number="0987654321",
        )

    def test_create_candidate(self):
        # Test creating a new candidate
        url = reverse("candidate-list")
        data = {
            "name": "Sita Devi",
            "age": 28,
            "gender": "Female",
            "email": "sita@example.com",
            "phone_number": "1122334455",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Sita Devi")

    def test_update_candidate(self):
        # Test updating a candidate
        url = reverse("candidate-detail", args=[self.candidate1.pk])
        data = {"age": 26}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["age"], 26)

    def test_delete_candidate(self):
        # Test deleting a candidate
        url = reverse("candidate-detail", args=[self.candidate1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_candidates(self):
        # Test searching for candidates
        url = reverse("candidate-search") + "?q=Ajay Yadav"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # It should return 2 results
        self.assertEqual(response.data[0]["name"], "Ajay Kumar Yadav")

    def test_search_multiple_spaces(self):
        # Test searching for candidates with multiple spaces between words
        url = reverse("candidate-search") + "?q=Ajay    Yadav"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust based on actual data
        self.assertEqual(response.data[0]["name"], "Ajay Kumar Yadav")

    def test_search_leading_trailing_spaces(self):
        # Test searching for candidates with spaces before or after the query
        url = reverse("candidate-search") + "?q=   Ajay Yadav   "
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust based on actual data
        self.assertEqual(response.data[0]["name"], "Ajay Kumar Yadav")

    def test_search_empty_query(self):
        # Test searching with an empty query
        url = reverse("candidate-search") + "?q="
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Search query is missing or only contains spaces"
        )

    def test_search_query_with_spaces(self):
        # Test searching with a query that contains only spaces
        url = reverse("candidate-search") + "?q=   "
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Search query is missing or only contains spaces"
        )

    def test_search_non_existing_word(self):
        # Test searching for candidates with one word that doesn't exist in the database
        url = reverse("candidate-search") + "?q=Ajay Zzzz"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_multiple_matching_words(self):
        # Test searching for candidates with multiple words that exist in different candidates
        url = reverse("candidate-search") + "?q=Ajay Kumar"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)

    def test_search_substring(self):
        # Test searching for candidates with a common substring in the name
        url = reverse("candidate-search") + "?q=Yad"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_search_special_characters(self):
        # Test searching for candidates with special characters in their name
        url = reverse("candidate-search") + "?q=Ajay@Yadav"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Ajay Kumar Yadav")
