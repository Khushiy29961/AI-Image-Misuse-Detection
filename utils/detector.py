import google.generativeai as genai

def perform_forensic_audit(image_data):
    """Uses Gemini 3 Flash to scan for deepfakes and anomalies."""
    model = genai.GenerativeModel('gemini-1.5-flash') # Using the stable flash model
    
    prompt = """
    Perform a professional forensic audit on this image. 
    1. Check for AI artifacts and skin texture inconsistencies.
    2. Audit lighting, shadows, and face-swap seams.
    3. Look for contextual anomalies like watermark date discrepancies.
    Provide a Risk Level (Low/Medium/High) and a detailed summary.
    """
    
    response = model.generate_content([prompt, image_data])
    return response.text