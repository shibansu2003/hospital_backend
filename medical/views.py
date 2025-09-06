from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Patient, Doctor, PatientDoctor
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorSerializer
from .permissions import IsOwnerForPatients, IsAuthenticatedOrReadDoctors

# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    """
    /api/patients/ (POST, GET)
    /api/patients/<id>/ (GET, PUT, DELETE)
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerForPatients]

    def get_queryset(self):
        # Only patients created by the authenticated user
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save()  # created_by handled in serializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    /api/doctors/ (POST*, GET)
    /api/doctors/<id>/ (GET, PUT*, DELETE*)
    * requires auth
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadDoctors]


class PatientDoctorViewSet(viewsets.ModelViewSet):
    """
    /api/mappings/ (POST -> assign; GET -> list all)
    /api/mappings/<id>/ (DELETE -> unassign)
    /api/mappings/<patient_id>/ (GET -> all doctors for a patient)
    """
    queryset = PatientDoctor.objects.select_related("patient", "doctor").all()
    serializer_class = PatientDoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Optionally filter by your patients only (safer for privacy)
        qs = self.queryset.filter(patient__created_by=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<patient_id>\d+)")
    def by_patient(self, request, patient_id=None):
        # Return all mappings for a specific patient YOU own
        patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
        qs = self.queryset.filter(patient=patient)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Enforce ownership on delete
        instance = self.get_object()
        if instance.patient.created_by_id != request.user.id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Assign doctor to patient
        return super().create(request, *args, **kwargs)


