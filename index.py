from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the chatbot
bot = ChatBot(
    "VehicleInsuranceBot",
    read_only=False,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I'm sorry, I couldn't understand that. Could you rephrase or ask about insurance options?",
            "maximum_similarity_threshold": 0.85,
        }
    ],
)

# Training data categorized by intent
insurance_data = [
    # General Conversation
    "Hi",
    "Hello! Welcome to [Insurance Company]. How can I assist you today? Options: - Get a Quote - Renew Policy - File a Claim - General Policy Information - Discounts and Offers",

    # Get a Quote
    "I want to get a quote",
    "Sure! To provide a quote, could you please share the make, model, and year of your vehicle?",
    "2020 Toyota Corolla",
    "Thank you! Could you also provide your zip code or location to calculate accurate rates?",
    "12345",
    "Got it! Do you want to add comprehensive coverage, or just liability coverage?",
    "Comprehensive coverage",
    "Excellent choice! Your estimated monthly premium is $120. Would you like to proceed with this quote?",

    # Renew Policy
    "I want to renew my policy",
    "I'd be happy to help! Please provide your policy number or registered email address.",
    "12345678",
    "Thank you! Your policy is eligible for renewal. Do you want to keep the current coverage or make changes?",
    "Keep current coverage",
    "Great! Your renewal request is processed. You'll receive a confirmation email shortly.",

    # File a Claim
    "I need to file a claim",
    "I'm sorry to hear that. Could you provide your policy number and a brief description of the incident?",
    "12345678",
    "Thank you. Could you also provide the date and location of the incident?",
    "Yesterday, Main Street",
    "Got it. Your claim has been initiated. A representative will contact you shortly for further details.",

    # Discounts and Offers
    "Can I get a discount?",
    "Yes! We offer discounts for safe driving records, multi-vehicle policies, and more. Are you a new customer or an existing one?",
    "New customer",
    "As a new customer, you're eligible for a 10% welcome discount! Would you like to learn about multi-policy discounts too?",
]


# Train the chatbot with the data
trainer = ListTrainer(bot)
trainer.train(insurance_data)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/get-response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")  # Get the user's message from the request
    if not user_input:
        return jsonify({"response": "Please type a message to get started."}), 400

    bot_response = bot.get_response(user_input)  # Get response from the chatbot

    # Add basic personalization
    if user_input.lower() in ["hi", "hello", "hey"]:
        bot_response = "Hello! Welcome to [Insurance Company]. How can I assist you today? Options: - Get a Quote - Renew Policy - File a Claim - General Policy Information - Discounts and Offers"

    return jsonify({"response": str(bot_response)})  # Return the response as JSON


if __name__ == "__main__":
    app.run(debug=True)

