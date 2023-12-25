# chatbot/views.py
import spacy
from django.http import JsonResponse
from django.shortcuts import render

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

def process_user_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Process user input with spaCy
        doc = nlp(user_input)

        # Your chatbot logic based on user input
        response = handle_user_input(doc)

        # You can return the response as JSON or render a template
        return JsonResponse({'response': response})

    return render(request, 'chatbot.html')

def handle_user_input(doc):
    # Your custom logic based on user input
    response = "I'm sorry, I didn't understand your request."

    # Check for specific keywords in user input
    if any(token.text.lower() in ['homestay', 'accommodation', 'stay'] for token in doc):
        response = "Certainly! We have various homestay options available. What preferences do you have?"

    # Check for specific keywords related to TravelNest
    if any(token.text.lower() in ['travelnest', 'what is travelnest'] for token in doc):
        response = "TravelNest is a platform that offers a wide range of accommodations and homestays. How can I assist you further?"

    # Add more conditions for other specific queries

    return response
