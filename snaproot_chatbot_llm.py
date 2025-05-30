# snaproot_chatbot_llm.py

import os
import sys
import openai

# Ensure your OpenAI API key is set in the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Calling the OpenAI API with a system and user prompt."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are SNAPROOT, a friendly assistant for SNAP EBT users."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def prompt_options(options):
    for key, desc in options.items():
        print(f"  {key}. {desc}")
    return input("Choose an option: ").strip()

def greet_and_authenticate(state):
    print("\nHello! I’m SNAPROOT. Let’s get you signed in with your SNAP EBT credentials.")
    input("Press Enter after completing authentication...")  # placeholder for real auth
    state['balance'] = 543
    print(f"Great, you’re authenticated. Your current EBT balance is ${state['balance']}.")
    print("\n[Endpoints] Continue | Help with authentication | Main Menu")
    input("Choose: ")

def first_time_vs_returning(state):
    ans = input("\nIs this your first time using SNAPROOT? (yes/no) ").strip().lower()
    if ans in ("yes", "y"):
        onboarding(state)
    else:
        daily_use_menu(state)

def onboarding(state):
    state['adults'] = input("How many adults are in your household? ").strip()
    state['children'] = input("How many children? ").strip()
    state['language'] = input("What language do you prefer? ").strip()
    state['cuisine_pref'] = input("Any favorite cuisines? ").strip()
    state['diet_restrictions'] = input("Any allergies or dietary restrictions? ").strip()
    print("Thanks! I’ve saved your preferences.")
    print("\n[Endpoints] Continue | Clarify onboarding | Main Menu")
    input("Choose: ")
    daily_use_menu(state)

def daily_use_menu(state):
    options = {
        '1': 'Plan meals for the week',
        '2': 'Recipe suggestions',
        '3': 'Find affordable groceries',
        '4': 'Nutrition insights',
        '5': 'Exit'
    }
    choice = prompt_options(options)
    if choice == '1':
        plan_meals(state)
    elif choice == '2':
        recipe_suggestions(state)
    elif choice == '3':
        grocery_finder(state)
    elif choice == '4':
        nutrition_insights(state)
    elif choice == '5':
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice.")
    daily_use_menu(state)

def plan_meals(state):
    budget = input(f"\nWhat budget for the week? [default ${state['balance']}] ").strip() or state['balance']
    meal_type = input("What kind of meals? (breakfast, lunch, dinner, snack) ").strip()
    prompt = (
        f"Generate a 7-day {meal_type} meal plan for a household with {state['adults']} adults and "
        f"{state['children']} children on a budget of ${budget}. Include estimated calories per meal."
    )
    result = call_llm(prompt)
    print("\n" + result)
    print("\n[Endpoints] Return to Menu | Adjust plan | Main Menu")
    input("Choose: ")

def recipe_suggestions(state):
    cuisine = input("\nWhich cuisine are you craving? ").strip()
    diet = input("Dietary focus (vegetarian, vegan, gluten-free, none)? ").strip()
    prompt = (
        f"Suggest 3–5 {cuisine} recipes suitable for {diet} diets. Include calorie count and macronutrient "
        "breakdown for each recipe."
    )
    result = call_llm(prompt)
    print("\n" + result)
    print("\n[Endpoints] Return to Menu | Refine suggestions | Main Menu")
    input("Choose: ")

def grocery_finder(state):
    location = input("\nWhere are you located? ").strip()
    prompt = (
        f"List 5 SNAP-eligible grocery items available near {location}. For each, give nutrition values "
        "and approximate price."
    )
    result = call_llm(prompt)
    print("\n" + result)
    print("\n[Endpoints] Return to Menu | Change location | Main Menu")
    input("Choose: ")

def nutrition_insights(state):
    metric = input("\nWhat would you like to check? (calories, protein, balance) ").strip().lower()
    prompt = f"Provide insights on {metric} for the user's current meal plan."
    result = call_llm(prompt)
    print("\n" + result)
    print("\n[Endpoints] Return to Menu | Explain metrics | Main Menu")
    input("Choose: ")

if __name__ == "__main__":
    state = {}
    greet_and_authenticate(state)
    first_time_vs_returning(state)

