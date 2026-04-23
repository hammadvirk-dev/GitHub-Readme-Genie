```python
import os
import time
import google.generativeai as genai

# --- CONFIGURATION ---
# The environment provides the API key via an empty string as per instructions
apiKey = "" 
genai.configure(api_key=apiKey)

def call_gemini_with_retry(prompt, system_instruction):
    """Implementation of exponential backoff for Gemini API calls."""
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-09-2025",
        system_instruction=system_instruction
    )
    
    retries = 5
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            if i == retries - 1:
                print("\n[Error] Could not connect to Gemini API after 5 attempts. Please check your connection.")
                return None
            wait_time = 2**i
            time.sleep(wait_time)

def get_user_input():
    """Collects user data to feed into the AI generator."""
    print("🧞‍♂️ Welcome to GitHub-Readme-Genie!")
    print("-----------------------------------")
    
    data = {}
    data['name'] = input("Enter your Full Name: ")
    data['role'] = input("What is your current role (e.g., Full Stack Developer): ")
    data['skills'] = input("Enter your skills (comma separated, e.g., Python, React, AWS): ")
    data['interests'] = input("What are you passionate about? (e.g., Open Source, AI, Web3): ")
    data['github_user'] = input("Your GitHub Username: ")
    data['linkedin'] = input("LinkedIn URL (Optional): ")
    data['twitter'] = input("Twitter URL (Optional): ")
    data['portfolio'] = input("Portfolio Website URL (Optional): ")
    
    return data

def generate_readme():
    user_data = get_user_input()
    
    system_prompt = (
        "You are a GitHub Profile Specialist. Your task is to generate a professional, "
        "aesthetic, and high-impact GitHub README.md file. Use Markdown syntax. "
        "Include shields.io badges for skills, GitHub Stats cards using 'github-readme-stats', "
        "and a clean layout with emojis."
    )
    
    user_prompt = f"""
    Create a GitHub Profile README for:
    Name: {user_data['name']}
    Role: {user_data['role']}
    Skills: {user_data['skills']}
    Interests: {user_data['interests']}
    GitHub Username: {user_data['github_user']}
    LinkedIn: {user_data['linkedin']}
    Twitter: {user_data['twitter']}
    Portfolio: {user_data['portfolio']}
    
    Instructions:
    1. Start with a high-quality heading and a dynamic bio.
    2. Create a 'Tech Stack' section with colorful badges from shields.io.
    3. Include a 'GitHub Stats' section using dynamic cards for stats and top languages.
    4. Include a 'Contact' section.
    5. Ensure the tone is professional yet engaging.
    """

    print("\n🧞‍♂️ Genie is working its magic...")
    result = call_gemini_with_retry(user_prompt, system_prompt)
    
    if result:
        filename = "GENERATED_README.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✨ Success! Your new README has been saved to {filename}")
        print("Copy the contents and paste them into your GitHub profile repository.")

if __name__ == "__main__":
    generate_readme()

```
  
