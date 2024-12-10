from django.db.models import Q, Count, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from django.db.models.functions import Coalesce
import re

class CandidateListCreateView(APIView):
    def post(self, request):
        # Create a new candidate record
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all candidates
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)


class CandidateDetailView(APIView):
    def put(self, request, pk):
        # Update an existing candidate by ID
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a candidate by ID
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(
                {"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND
            )

        candidate.delete()
        return Response(
            {"message": "Candidate deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CandidateSearchView(APIView):
    def get(self, request):
        # Search candidates based on name
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response(
                {"error": "Search query is missing or only contains spaces"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        query = re.sub(r"[^a-zA-Z0-9 ]", " ", query)
        search_words = query.split()

        # Build the filter for partial matches
        filters = Q()
        for word in search_words:
            filters |= Q(name__icontains=word)

        # Annotate candidates with relevancy score and sort by it
        candidates = (
            Candidate.objects.filter(filters)
            .annotate(
                relevancy=Count("id", filter=Q(name__icontains=search_words[0]))
                + sum(
                    Count("id", filter=Q(name__icontains=word))
                    for word in search_words[1:]
                )
            )
            .order_by("-relevancy")
        )
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
