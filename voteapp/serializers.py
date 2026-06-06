from rest_framework import serializers

from .models import (
    Staff,
    ElectionLocation,
    People,
    Candidate,
    ElectionSettings,
    Vote
)


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"


class ElectionLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectionLocation
        fields = "__all__"


class PeopleSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(
        use_url=True
    )

    class Meta:
        model = People
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = "__all__"


class ElectionSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectionSettings
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = "__all__"