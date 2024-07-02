from rest_framework import serializers

from .models import Job, Category , Employee , Document
from scrape.models import SectorCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title',)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'position_salary',
            'position_location',
            'company_name',
            'created_at_formatted'
        )


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'category',
            'title',
            'description',
            'position_salary',
            'position_location',
            'company_name',
            'company_location',
            'company_email',
            'created_at_formatted'
        )


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
            'matricule',
            'phone',
            'description',
        )
        read_only_fields = ('created_at_formatted',)



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'created_by',
            'employee',
            'document',
            'is_email_delivered',
            'is_whatsapp_delivered',
            'uploaded_at',
            'uploaded_at_formatted'
            
        )


class CategoryViewSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = SectorCategory
        fields = ['id', 'name', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        # Get all subcategories recursively
        subcategories = SectorCategory.objects.filter(parent=obj)
        serializer = CategoryViewSerializer(subcategories, many=True)
        return serializer.data