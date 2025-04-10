# core/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response

class BaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"EC": 0, "EM": "Success", "DT": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"EC": 0, "EM": f"{self.queryset.model.__name__} created successfully", "DT": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"EC": 1, "EM": "Validation error", "DT": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"EC": 0, "EM": "Success", "DT": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"EC": 0, "EM": f"{self.queryset.model.__name__} updated successfully", "DT": serializer.data}, status=status.HTTP_200_OK)
        return Response({"EC": 1, "EM": "Validation error", "DT": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"EC": 0, "EM": f"{self.queryset.model.__name__} deleted successfully", "DT": None}, status=status.HTTP_200_OK)
