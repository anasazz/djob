from rest_framework import serializers

from scrape.models import ScrapedData

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'title',)


class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = "__all__"


class ScrapedDataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
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

