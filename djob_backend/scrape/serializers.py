from rest_framework import serializers

from scrape.models import ScrapedData
from rest_framework import serializers
from .models import ScrapedData
from datetime import timedelta

class ScrapedDataSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()
    publie_le_humanized = serializers.SerializerMethodField()
    date_limite_humanized = serializers.SerializerMethodField()

    class Meta:
        model = ScrapedData
        fields = ['id', 'reference','caution_provisoire','estimation', 'acheteur_public', 'categorie', 'publie_le', 'date_limite', 'objet',
                  'lieu_execution', 'org', 'reference_hash', 'time_left', 'publie_le_humanized', 'date_limite_humanized']

        depth=1
    def get_time_left(self, obj):
        time_left = obj.time_left()  # Assuming this method exists in your model to calculate time left
        if time_left:
            months = time_left.days // 30
            remaining_days = time_left.days % 30
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            time_left_str = ""
            if months > 0:
                time_left_str += f"{months} mois "
            if remaining_days > 0:
                time_left_str += f"{remaining_days} jours "
            if hours > 0:
                time_left_str += f"{hours} heures"

            # Remove trailing space if exists
            time_left_str = time_left_str.strip()

            return time_left_str if time_left_str else None

        return None

    def get_publie_le_humanized(self, obj):
        if obj.publie_le:
            return obj.publie_le.strftime('%d %B %Y')  # Format as desired, e.g., '31 January 2024'

        return None

    def get_date_limite_humanized(self, obj):
        if obj.date_limite:
            return obj.date_limite.strftime('%d %B %Y %H:%M')  # Format as desired, e.g., '31 January 2024 14:30'

        return None
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'title',)




class ScrapedDataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = "__all__"
        depth=1

