from django.shortcuts import render
import json
import random
from django.http import JsonResponse
from homestay.models import HomeStay, Feature
from django.urls import reverse


# Create your views here.


def extract_info(input_str):
    # Remove hyphens from the input for better processing
    input_str = input_str.replace('-', '').rstrip('s').lower()
    input_words = input_str.split()

    # Fetch all unique locations and features from the HomeStay model
    all_locations = HomeStay.objects.values_list('location', flat=True).distinct()
    print(f"All Location: {all_locations}")

    # Fetch all unique feature names from the Feature model
    all_features = Feature.objects.values_list('name', flat=True).distinct()
    print(f"All Features: {all_features}")

    # Find locations and features
    locations = []
    features = []

    i = 0
    while i < len(input_words):
        word = input_words[i]

        # Check if the current word is a location
        if any(word.lower() == location.lower().replace('-', '') for location in all_locations):
            matched_location = next((location for location in all_locations if word.lower() == location.lower().replace('-', '')), None)
            if matched_location:
                locations.append(matched_location)
            i += 1

        # Check if the current and next words form a multi-word feature
        elif i < len(input_words) - 1 and any(f"{word.lower()} {input_words[i + 1]}".lower() == feature.lower() or
                                              f"{word.lower()} {input_words[i + 1]}".lower() == feature.lower().replace('-', '')
                                              for feature in all_features):
            features.append(f"{word} {input_words[i + 1]}")
            i += 2

        # Check if the current word is a single-word feature
        elif any(word.lower() == feature.lower() or word.lower() == feature.lower().replace('-', '') for feature in all_features):
            matched_feature = next((feature for feature in all_features if word.lower() == feature.lower() or word.lower() == feature.lower().replace('-', '')), None)
            if matched_feature:
                features.append(matched_feature)
            i += 1

        else:
            i += 1

    print(f"Extracted Locations: {locations}")
    print(f"Extracted Features: {features}")

    # Find check-in and check-out dates
    check_in_date = None
    check_out_date = None
    for word in input_words:
        if '-' in word:
            dates = word.split('-')
            if len(dates) == 2:
                check_in_date, check_out_date = dates
                break

    return locations, features, check_in_date, check_out_date




def search_homestays(locations, features, check_in_date, check_out_date):
    # Start with a queryset that includes all Homestays
    homestays = HomeStay.objects.all()

    # Filter based on the provided locations (case-insensitive)
    if locations:
        locations_regex = '|'.join(locations)
        homestays = homestays.filter(location__iregex=locations_regex)

    # Filter based on the provided features
    if features:
        features_regex = '|'.join(features)
        homestays = homestays.filter(features__name__iregex=features_regex)

    # You might want to add more filters based on check-in and check-out dates
    # For simplicity, assuming check_in_date and check_out_date are DateField in your model
    if check_in_date:
        homestays = homestays.filter(check_in_date__lte=check_in_date)

    if check_out_date:
        homestays = homestays.filter(check_out_date__gte=check_out_date)

    return homestays




def chatbot(request):
    user_input = request.GET.get('user_input', '').lower()  # Assuming the user input is passed as a parameter

    # Load intents from the JSON file
    with open('intents.json', 'r') as file:
        intents = json.load(file)['intents']

    # Find the matching intent
    matched_intent = next((intent for intent in intents if any(pattern in user_input for pattern in intent['patterns'])), None)

    # Check if the user has the "booking" tag
    if matched_intent and matched_intent['tag'] == 'booking':
        locations, features, check_in_date, check_out_date = extract_info(user_input)

        # Check if the user has provided information about the homestay
        if locations and features and check_in_date and check_out_date:
            # Search for homestays based on the provided attributes
            homestays = search_homestays(locations, features, check_in_date, check_out_date)

            if homestays.exists():
                homestay_details = [
                    {
                        'name': homestay.name,  # Replace with the actual field name
                        'location': homestay.location,
                        'features': [feature.name for feature in homestay.features.all()],  # Replace with the actual field name
                        'id' : homestay.id
                        # Add more fields as needed
                    }
                    for homestay in homestays
                ]
                homestay_responses = [
                    f"<a href='{homestay_detail_url(homestay.id)}'>{homestay.name}</a> - {homestay.location}"
                    for homestay in homestays
                ]
                response = f"I found homestays that match your criteria. Here are some options: {'<br>'.join(homestay_responses)}"
            else:
                response = "I'm sorry, but I couldn't find any homestays that match your criteria. Please try again with different preferences."
        else:
            # Check if only features are provided
            if features:
                homestays = search_homestays([], features, None, None)

                if homestays.exists():
                    homestay_details = [
                        {
                            'name': homestay.name,  # Replace with the actual field name
                            'location': homestay.location,
                            'features': [feature.name for feature in homestay.features.all()],
                            'id' : homestay.id  # Replace with the actual field name
                            # Add more fields as needed
                        }
                        for homestay in homestays
                    ]
                    homestay_responses = [
                    f"<a href='{homestay_detail_url(homestay.id)}'>{homestay.name}</a> - {homestay.location}"
                    for homestay in homestays
                ]
                response = f"I found top homestays that match your criteria. Here are some options: {'<br>'.join(homestay_responses)}"
                response = "I'm sorry, but I couldn't find any homestays with the specified features. Please try again with different details."
            else:
                response = "Sure, I can help you with booking a homestay. Please provide information about the homestay's location, features, check-in, and check-out dates."

    else:
        # Check if the user is providing information about the homestay in subsequent input
        locations, features, check_in_date, check_out_date = extract_info(user_input)

        # Check if the user provided information about the homestay
        if locations or features or check_in_date or check_out_date:
            # Search for homestays based on the provided attributes
            homestays = search_homestays(locations, features, check_in_date, check_out_date)

            if homestays.exists():
                # You can customize the response based on the search results
                homestay_details = [
                    {
                        'name': homestay.name,  # Replace with the actual field name
                        'location': homestay.location,
                        'features': [feature.name for feature in homestay.features.all()],  # Replace with the actual field name
                        'id': homestay.id
                        # Add more fields as needed
                    }
                    for homestay in homestays
                ]
                homestay_responses = [
                    f"<a href='{homestay_detail_url(homestay.id)}'>{homestay.name}</a> - {homestay.location}"
                    for homestay in homestays
                ]
                response = f"I found top 5 homestays that match your criteria. Here are some options: {'<br>'.join(homestay_responses)}"
            else:
                response = "I'm sorry, but I couldn't find any homestays that match the provided information. Please try again with different details."
        else:
            # Get a response based on the matched intent or use a default response
            response = random.choice(matched_intent['responses']) if matched_intent else "I'm sorry, I didn't understand that. Can you please rephrase?"

    return JsonResponse({'response': response, 'matched_intent': matched_intent})


def chat(request):
    return render(request, 'chatbot.html')


def homestay_detail_url(homestay_id):
    return reverse('detail', args=[homestay_id])