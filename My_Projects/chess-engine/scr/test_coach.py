# """Quick test to check if Gemini API works"""
# from google import genai

# API_KEY = "AQ.Ab8RN6L2lSOull50FGjJpR5JDXIOGclLbfz_cAMfYk4a03jRYQ"

# def test():
#     try:
#         client = genai.Client(api_key=API_KEY)
        
#         print("Testing connection...")
        
#         # Try different model names
#         models_to_try = [
#             'gemini-1.5-flash',
#             'gemini-2.0-flash',
#             'gemini-1.5-pro',
#             'models/gemini-1.5-flash',
#             'models/gemini-2.0-flash',
#         ]
        
#         for model in models_to_try:
#             try:
#                 response = client.models.generate_content(
#                     model=model,
#                     contents="Say 'Hello' in 2 words."
#                 )
#                 print(f"SUCCESS with model: {model}")
#                 print(f"Response: {response.text}")
#                 print("\nUse this model name in coach.py!")
#                 return model
#             except Exception as e:
#                 print(f"Failed with {model}: {e}")
#                 continue
        
#         print("\nAll models failed.")
#         return None
    
#     except Exception as e:
#         print(f"Connection error: {e}")
#         return None

# if __name__ == "__main__":
#     test()

from google import genai
client = genai.Client(api_key="AQ.Ab8RN6KZHf-B8GhY1PDtWOM9zFFw3O-ECHNuzoCA60QcAY6r-Q")
response = client.models.generate_content(model='gemini-2.5-flash', contents='Say hello')
print(response.text)