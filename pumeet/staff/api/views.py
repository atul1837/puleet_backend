from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from pumeet.candidate_profile.models import Profile
from pumeet.seat_management.models import Allotment, Branch, Preference
from pumeet.staff.services.allotment import allot_branches_based_on_preferences_and_rank

User = get_user_model()


class CandidateListView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = self.OutputSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CandidateView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = "__all__"

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(
                "Candidate Profile does not exist", status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.OutputSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(
                "Candidate Profile does not exist", status=status.HTTP_404_NOT_FOUND
            )
        profile.delete()
        return Response("Candidate Profile deleted", status=status.HTTP_200_OK)


class CandidateApproveApi(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(
                "Candidate Profile does not exist", status=status.HTTP_404_NOT_FOUND
            )
        profile.approved = True
        profile.save()
        return Response("Candidate approved", status=status.HTTP_200_OK)


class CandidateRejectApi(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(
                "Candidate Profile does not exist", status=status.HTTP_404_NOT_FOUND
            )
        profile.submitted = False
        profile.approved = False
        profile.save()
        return Response("Candidate rejected", status=status.HTTP_200_OK)


class PreferenceStaffView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class InputSerializer(serializers.Serializer):
        user = serializers.UUIDField(required=True)
        branch = serializers.UUIDField(required=True)
        preference = serializers.IntegerField(required=True)

    class OutputSerializer(serializers.ModelSerializer):

        branch = serializers.SerializerMethodField()

        class Meta:
            model = Preference
            fields = ("id", "created_on", "updated_on", "preference", "branch", "user")

        def get_branch(self, obj):
            if not obj.branch:
                return None
            return {"id": obj.branch.id, "name": obj.branch.branch_name}

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            preferences = Preference.objects.filter(user=user)
            serializer = self.OutputSerializer(preferences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            return Response(
                "User's Preferences does not exist", status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            Preference.objects.filter(user=user).delete()
            return Response(
                "Preferences deleted successfully", status=status.HTTP_200_OK
            )
        except Preference.DoesNotExist:
            return Response(
                "Preferences does not exist", status=status.HTTP_404_NOT_FOUND
            )


class BranchView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class InputSerializer(serializers.Serializer):
        branch_name = serializers.CharField(required=True)
        total_seats = serializers.IntegerField(required=True)
        general_seats = serializers.IntegerField(required=True)
        sc_seats = serializers.IntegerField(required=True)
        st_seats = serializers.IntegerField(required=True)

    def post(self, request, format=None):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Branch.objects.create(
                branch_name=serializer.validated_data["branch_name"],
                total_seats=serializer.validated_data["total_seats"],
                general_seats=serializer.validated_data["general_seats"],
                sc_seats=serializer.validated_data["sc_seats"],
                st_seats=serializer.validated_data["st_seats"],
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response("Branch created successfully", status=status.HTTP_200_OK)


class AllotBranchesApi(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, format=None):
        try:
            allot_branches_based_on_preferences_and_rank()
            return Response("Branches allotted successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AllotBranchesListApi(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class OutputSerializer(serializers.ModelSerializer):

        branch = serializers.SerializerMethodField()
        user = serializers.SerializerMethodField()
        preference = serializers.SerializerMethodField()

        class Meta:
            model = Allotment
            fields = (
                "id",
                "created_on",
                "updated_on",
                "branch",
                "user",
                "preference",
                "allotment_category",
            )

        def get_branch(self, obj):
            if not obj.branch:
                return None
            return {"id": obj.branch.id, "name": obj.branch.branch_name}

        def get_user(self, obj):
            if not obj.user:
                return None
            return {"id": obj.user.id, "email": obj.user.email}

        def get_preference(self, obj):
            if not obj.preference:
                return None
            return {"id": obj.preference.id, "preference": obj.preference.preference}

    def get(self, request, format=None):
        try:
            allotments = Allotment.objects.all()
            serializer = self.OutputSerializer(allotments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
