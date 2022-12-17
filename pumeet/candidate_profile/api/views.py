from rest_framework import permissions, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from pumeet.candidate_profile.models import Profile

class ProfileDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        father_name = serializers.CharField(required=False)
        mother_name = serializers.CharField(required=False)
        date_of_birth = serializers.DateField(required=False)
        category = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        mobile_no = serializers.CharField(required=False)
        gender = serializers.CharField(required=False)
        nationality = serializers.CharField(required=False)
        correspondance_address = serializers.CharField(required=False)
        permanent_address = serializers.CharField(required=False)
        state = serializers.CharField(required=False)
        tenth_board = serializers.CharField(required=False)
        tenth_marks = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
        tenth_passing_year = serializers.IntegerField(required=False)
        tenth_certificate = serializers.FileField(required=False)
        twelveth_board = serializers.CharField(required=False)
        twelveth_marks = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
        twelveth_passing_year = serializers.IntegerField(required=False)
        twelveth_certificate = serializers.FileField(required=False)
        diploma_branch = serializers.CharField(required=False)
        diploma_passing_year = serializers.IntegerField(required=False)
        diploma_board = serializers.CharField(required=False)
        diploma_marks = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
        diploma_institute = serializers.CharField(required=False)
        diploma_certificate = serializers.FileField(required=False)
        all_india_rank = serializers.IntegerField(required=False)
        application_number = serializers.CharField(required=False)
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = (
                "name",
                "father_name",
                "mother_name",
                "date_of_birth",
                "category",
                "email",
                "mobile_no",
                "gender",
                "nationality",
                "correspondance_address",
                "permanent_address",
                "state",
                "tenth_board",
                "tenth_marks",
                "tenth_passing_year",
                "tenth_certificate",
                "twelveth_board",
                "twelveth_marks",
                "twelveth_passing_year",
                "twelveth_certificate",
                "diploma_branch",
                "diploma_passing_year",
                "diploma_board",
                "diploma_marks",
                "diploma_institute",
                "diploma_certificate",
                "all_india_rank",
                "application_number",
            )

        def get_tenth_certificate(self, obj):
            if obj.tenth_certificate:
                return obj.tenth_certificate.url
            return None

        def get_twelveth_certificate(self, obj):
            if obj.twelveth_certificate:
                return obj.twelveth_certificate.url
            return None

        def get_diploma_certificate(self, obj):
            if obj.diploma_certificate:
                return obj.diploma_certificate.url
            return None


    def get(self, request, format=None):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            serializer = self.OutputSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response("Profile does not exist", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            profile = Profile.objects.get(user=user)
            for value in serializer.validated_data:
                if serializer.validated_data[value] is not None:
                    setattr(profile, value, serializer.validated_data[value])
            profile.save()
            return Response("Profile updated successfully", status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user, **serializer.validated_data)
            return Response("Profile created successfully", status=status.HTTP_201_CREATED)


    def delete(self, request, format=None):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
            profile.delete()
            return Response("Profile deleted successfully", status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response("Profile does not exist", status=status.HTTP_404_NOT_FOUND)
