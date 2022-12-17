from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from pumeet.seat_management.models import Preference, Branch, Allotment
from django.contrib.auth import get_user_model

User = get_user_model()

# Public API
class BranchListView(APIView):
    permission_classes = (permissions.AllowAny,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Branch
            fields = "__all__"

    def get(self, request, format=None):
        branches = Branch.objects.all()
        serializer = self.OutputSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PreferenceListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):

        branch = serializers.SerializerMethodField()

        class Meta:
            model = Preference
            fields = ("id", "created_on", "updated_on", "preference", "branch", "user")

        def get_branch(self, obj):
            if not obj.branch:
                return None
            return {"id": obj.branch.id, "name": obj.branch.branch_name}

    def get(self, request, format=None):
        user = request.user
        try:
            preferences = Preference.objects.filter(user=user).select_related("branch")
            serializer = self.OutputSerializer(preferences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            return Response(
                "User's Preferences does not exist", status=status.HTTP_404_NOT_FOUND
            )


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
            return Response(
                "Preference updated successfully", status=status.HTTP_200_OK
            )
        except Preference.DoesNotExist:
            preference = Preference.objects.create(
                user=user,
                branch=branch,
                preference=serializer.validated_data["preference"],
            )
            return Response(
                "Preference created successfully", status=status.HTTP_200_OK
            )

    def delete(self, request, format=None):
        user = request.user
        try:
            preferences = Preference.objects.filter(user=user)
            preferences.delete()
            return Response(
                "Preferences deleted successfully", status=status.HTTP_200_OK
            )
        except Preference.DoesNotExist:
            return Response(
                "Preferences does not exist", status=status.HTTP_404_NOT_FOUND
            )


class AllotmentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Allotment
            fields = "__all__"

    def get(self, request, format=None):
        user = request.user
        try:
            allotments = Allotment.objects.get(user=user)
        except Allotment.DoesNotExist:
            return Response(
                "User's Allotments does not exist", status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.OutputSerializer(allotments)
        return Response(serializer.data, status=status.HTTP_200_OK)
