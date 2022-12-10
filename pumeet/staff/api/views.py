from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from pumeet.seat_management.models import Preference
from pumeet.seat_management.models import Branch
from django.contrib.auth import get_user_model

User = get_user_model()

class PreferenceStaffView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    class InputSerializer(serializers.Serializer):
        user = serializers.UUIDField(required=True)
        branch = serializers.UUIDField(required=True)
        preference = serializers.IntegerField(required=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Preference
            fields = "__all__"

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
            return Response("User's Preferences does not exist", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            Preference.objects.filter(user=user).delete()
            return Response("Preferences deleted successfully", status=status.HTTP_200_OK)
        except Preference.DoesNotExist:
            return Response("Preferences does not exist", status=status.HTTP_404_NOT_FOUND)


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