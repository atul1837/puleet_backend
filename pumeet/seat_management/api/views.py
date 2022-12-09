from rest_framework import permissions, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from pumeet.candidate_profile.models import Profile
from pumeet.seat_management.models import Preference
from pumeet.seat_management.models import Branch

class PreferenceListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Preference
            fields = "__all__"


    def get(self, request, format=None):
        user = request.user
        try:
            preferences = Preference.objects.filter(user=user)
            serializer = self.OutputSerializer(preferences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            return Response("User's Preferences does not exist", status=status.HTTP_404_NOT_FOUND)


class PreferenceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        branch = serializers.UUIDField(required=True)
        preference = serializers.IntegerField(required=True)

    def post(self, request, format=None):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:        
            branch = Branch.objects.get(id=serializer.validated_data["branch"])
        except Branch.DoesNotExist:
            return Response("Branch does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            preference = Preference.objects.get(user=user, branch=branch)
            preference.preference = serializer.validated_data["preference"]
            preference.save()
            return Response("Preference updated successfully", status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            preference = Preference.objects.create(user=user, branch=branch, preference=serializer.validated_data["preference"])
            return Response("Preference created successfully", status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:        
            branch = Branch.objects.get(id=serializer.validated_data["branch"])
        except Branch.DoesNotExist:
            return Response("Branch does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            preference = Preference.objects.get(user=user, branch=branch, preference=serializer.validated_data["preference"])
            preference.delete()
            return Response("Preference deleted successfully", status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            return Response("Preference does not exist", status=status.HTTP_404_NOT_FOUND)