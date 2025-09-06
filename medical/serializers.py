from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "age", "gender", "address", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "email", "phone", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_email(self, value):
        # On update, allow the same instance to keep its email
        instance = getattr(self, "instance", None)
        qs = Doctor.objects.filter(email__iexact=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["created_by"] = user
        return super().create(validated_data)


class PatientDoctorSerializer(serializers.ModelSerializer):
    # useful nested info (read-only)
    patient_name = serializers.ReadOnlyField(source="patient.name")
    doctor_name = serializers.ReadOnlyField(source="doctor.name")
    doctor_specialization = serializers.ReadOnlyField(source="doctor.specialization")

    class Meta:
        model = PatientDoctor
        fields = [
            "id",
            "patient",
            "doctor",
            "patient_name",
            "doctor_name",
            "doctor_specialization",
            "assigned_by",
            "assigned_at",
        ]
        read_only_fields = ["id", "assigned_by", "assigned_at"]

    def validate(self, attrs):
        # Ensure the current user owns the patient when assigning
        request = self.context["request"]
        patient = attrs.get("patient")
        if patient.created_by_id != request.user.id:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return attrs

    def create(self, validated_data):
        validated_data["assigned_by"] = self.context["request"].user
        return super().create(validated_data)
