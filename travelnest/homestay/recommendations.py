from math import sqrt
from .models import Feature, HomeStay
from booking.models import Booking

class RecommendationSystem:
    def __init__(self, homestays):
        self.homestays = homestays
        self.feature_vector_length = len(Feature.objects.all()) + 1 

    def recommend_homestays(self, user_liked_homestays, user_past_bookings):
        user_vector = self.generate_user_vector(user_liked_homestays, user_past_bookings)

        recommendations = []

        for homestay in self.homestays:
            homestay_vector = self.generate_homestay_vector(homestay, user_past_bookings)
            similarity = self.calculate_cosine_similarity(user_vector, homestay_vector)

            print(f"Cosine Similarity for Homestay '{homestay.name}': {similarity}")

            recommendations.append({'homestay': homestay, 'similarity': similarity})

        recommendations.sort(key=lambda x: x['similarity'], reverse=True)
        return recommendations

    def generate_user_vector(self, user_liked_homestays, user_past_bookings):
        user_vector = []

        for feature in Feature.objects.all():
            feature_value = 1 if user_liked_homestays.filter(features=feature).exists() else 0
            user_vector.append(feature_value)

        # Extract location information from liked homestays
        liked_homestay_location = (
            user_liked_homestays.first().location
            if user_liked_homestays.exists()
            else None
        )
        user_vector.append(1 if liked_homestay_location else 0)

        # Extract location information from past bookings (you may need to adjust this based on your data structure)
        user_location = (
            user_past_bookings.first().homestay.location
            if user_past_bookings.exists()
            else None
        )
        user_vector.append(1 if user_location else 0)

        # Normalize the vector
        user_vector = [value / self.feature_vector_length for value in user_vector]

        print(f"Cosine Similarity for Homestay : {user_vector}")
        return user_vector

    def generate_homestay_vector(self, homestay, user_past_bookings):
        homestay_vector = []

        for feature in Feature.objects.all():
            feature_value = 1 if homestay.features.filter(pk=feature.pk).exists() else 0
            homestay_vector.append(feature_value)

        # Extract location information from past bookings (you may need to adjust this based on your data structure)
        homestay_location = user_past_bookings.first().homestay.location if user_past_bookings.exists() else None
        homestay_vector.append(1 if homestay_location else 0)

        # Normalize the vector
        homestay_vector = [value / self.feature_vector_length for value in homestay_vector]

        return homestay_vector

    def calculate_cosine_similarity(self, vector1, vector2):
        dot_product = sum(x * y for x, y in zip(vector1, vector2))
        magnitude1 = sqrt(sum(x ** 2 for x in vector1))
        magnitude2 = sqrt(sum(x ** 2 for x in vector2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        else:
            return dot_product / (magnitude1 * magnitude2)
