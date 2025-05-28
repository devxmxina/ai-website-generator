# utils/ai_generator.py
import google.generativeai as genai
import json # for validating JSON before returning (optional but useful)

# genai.configure(api_key=api_key) will be in main.py

def generate_website_data(user_inputs, translator): # api_key is no longer passed here
    model = genai.GenerativeModel("gemini-1.5-flash")

    company = user_inputs.get('company_name', 'N/A')
    industry = user_inputs.get('industry', 'N/A')
    content_source = user_inputs.get('content_source', 'generate')
    description = user_inputs.get('description', '')
    ai_should_suggest_description = user_inputs.get('ai_should_suggest_description', False)
    generate_logo_concept = user_inputs.get('generate_logo_concept', False)
    has_brand_book = user_inputs.get('has_brand_book', False)
    visual_style = user_inputs.get('visual_style', 'Modern')
    num_pages_input = user_inputs.get('num_pages', 3) # Either a number or "AI_DECIDES"
    icon_style = user_inputs.get('icon_style', 'Flat')
    button_shape = user_inputs.get('button_shape', 'Rounded')
    image_style_preferences = user_inputs.get('image_style_preferences', [])

    # Forming the main description for the AI
    if ai_should_suggest_description or not description:
        main_description = f"The user has not provided a detailed description. Generate content for a '{industry}' company specializing in typical services/products for that industry, aiming for a '{visual_style}' visual style. The company name is '{company}'."
    else:
        main_description = description

    # Determining the number of pages
    if num_pages_input == "AI_DECIDES":
        pages_instruction = "You decide the optimal number of pages (typically 3-7) based on the industry and project type. Suggest common and essential pages."
        # For the JSON request, if AI decides, it should insert the number of pages into its response,
        # but we can also ask it to specify how many it decided to generate in a separate field.
        # For simplicity, let's just ask it to generate them.
    else:
        pages_instruction = f"Generate exactly {num_pages_input} page objects."



    

    prompt = f"""
You are an expert AI Website Architect and Content Strategist. Your task is to generate a comprehensive, structured JSON output for a new website based on the user's requirements.
The JSON output must be a single, valid JSON object. Do not include any explanatory text, comments, or markdown formatting before or after the JSON object itself.

**CRITICAL JSON FORMATTING RULES TO FOLLOW - ADHERE STRICTLY:**
1.  **Commas in Objects:** ALL key-value pairs within an object (e.g., "key1": "value1", "key2": "value2") MUST be separated by a comma (,), EXCEPT for the VERY LAST pair in that specific object.
2.  **Commas in Arrays:** ALL elements within an array (e.g., [{{ "id": 1 }}, {{ "id": 2 }}]) MUST be separated by a comma (,), EXCEPT for the VERY LAST element in that array.
3.  **Array Structure:** Arrays MUST be standard JSON arrays of objects or values (e.g., "pages": [ {{...}}, {{...}} ] or "tags": ["tag1", "tag2"]). DO NOT use object-like structures with numeric keys for array elements (e.g., AVOID "pages": {{ "0": {{...}}, "1": {{...}} }} - THIS IS WRONG).
4.  **Quotes:** ALL keys (property names) and ALL string values MUST be enclosed in double quotes (e.g., "key": "value").
5.  **Numeric Values:** Numeric values should NOT be enclosed in quotes (e.g., "count": 10, "isActive": true, "price": 29.99). Example: "base_font_size_px": 16 (NOT "16").
6.  **No Trailing Commas:** Do NOT use trailing commas after the last element in an array or the last key-value pair in an object.
7.  **Matching Brackets/Braces:** Ensure all opening brackets `[` and braces `{{` have a corresponding closing bracket `]` or brace `}}`.

User Requirements:
- Company Name: {company}
- Industry: {industry}
- Content Source: {content_source} (If 'generate', create compelling text. If 'provide_later', create relevant placeholder text like "[User to provide specific service details here]").
- Project Description: {main_description}
- AI Should Suggest Description (if user didn't provide): {ai_should_suggest_description}
- Generate Logo Concept: {generate_logo_concept}
- Has Existing Brand Book: {has_brand_book} (If true, AI should suggest styles that are flexible enough to adapt; if false, AI has more freedom).
- Desired Visual Style: {visual_style}
- Number of Pages: {pages_instruction}
- Preferred Icon Style: {icon_style}
- Preferred Button Shape: {button_shape}
- Preferred Image Characteristics: {', '.join(image_style_preferences) if image_style_preferences else 'Not specified, use industry best practices.'}

JSON Output Structure:
The root JSON object must contain three top-level keys: "project_overview", "pages", and "global_style".

1.  "project_overview": An object containing:
    *   "company_name": "{company}"
    *   "industry": "{industry}"
    *   "ai_generated_project_summary": (If {ai_should_suggest_description} is true or description was empty) A concise, AI-generated summary of the project's purpose and target audience (2-3 sentences). If user provided a description, this can be a refined version or a brief comment.
    *   "suggested_tagline": A catchy tagline for the website.
    *   "logo_concept_suggestion": (If {generate_logo_concept} is true) A brief textual description of a logo concept (e.g., "Minimalist abstract mark representing growth, using primary and accent colors. Typeface: a modern sans-serif."). If false, value should be "User will provide logo."

2.  "pages": An array of page objects. The number of pages should follow the '{pages_instruction}'.
    *   Each page object must have:
        *   "page_id": A unique kebab-case identifier (e.g., "home", "about-us", "services-overview").
        *   "page_title": A user-friendly, SEO-friendly title for the page (e.g., "Welcome to {company}", "About Our Team", "Our Expert Services").
        *   "sections": An array of 2 to 4 section objects.
            *   Each section object must have:
                *   "section_id": A unique kebab-case identifier for the section within the page (e.g., "hero-banner", "key-features", "client-testimonials").
                *   "section_type": A semantic type (e.g., "hero", "features_grid", "text_with_image", "call_to_action_banner", "team_gallery", "pricing_table", "contact_form_map").
                *   "content": An object with:
                    *   "headline": A strong, engaging headline (max 70 characters).
                    *   "subheadline": (Optional) A supporting subheadline or brief explanation (max 150 characters).
                    *   "body_text": The main text content for the section. If content_source is 'generate', write compelling copy. If 'provide_later', use descriptive placeholders like "[Client to provide details on Feature 1, highlighting its benefits.]". (Max 300 characters, or more if it's a primary content block like "About Us full text").
                    *   "image_placeholder_description": (Optional) A description of a suitable image for this section, considering '{', '.join(image_style_preferences) if image_style_preferences else 'industry best practices'}'. (e.g., "Bright photo of a diverse team collaborating in a modern office.", "Abstract background texture in primary color.").
                    *   "cta_button": (Optional) An object with:
                        *   "text": Call-to-action button text (e.g., "Learn More", "Get Quote").
                        *   "link_suggestion": A suggested internal page link (e.g., "#services-overview", "/contact-us").
                *   "layout_suggestion": A descriptive name for a common layout pattern (e.g., "hero_image_left_text_right", "three_column_grid_with_icons", "alternating_image_text_rows", "full_width_banner_centered_text").
                *   "background_suggestion": (Optional) Suggestion for background: "color_primary", "color_secondary", "color_background", "image_subtle_pattern", "image_full_bleed".

3.  "global_style": An object describing the overall visual design system.
    *   "color_palette": An object with specific roles:
        *   "primary": Hex color code.
        *   "secondary": Hex color code.
        *   "accent": Hex color code.
        *   "neutral_dark": Hex color code (for dark text, backgrounds).
        *   "neutral_light": Hex color code (for light text, backgrounds, dividers).
        *   "background_page": Hex color code for default page background.
        *   "success": Hex color code.
        *   "error": Hex color code.
        (Generate these colors based on the industry: '{industry}', visual style: '{visual_style}'.)
    *   "typography": An object with:
        *   "heading_font": Font family (e.g., "Montserrat, sans-serif").
        *   "body_font": Font family (e.g., "Lato, sans-serif").
        *   "base_font_size_px": Base font size in pixels (e.g., 16).
    *   "buttons": An object with:
        *   "shape": "{button_shape}" (user input).
        *   "default_style_description": Brief description (e.g., "Solid primary color background, white text, slight shadow on hover").
    *   "icons": An object with:
        *   "style": "{icon_style}" (user input).
        *   "usage_suggestion": Brief suggestion (e.g., "Use consistently for feature lists and navigation elements").
    *   "image_guidelines": Brief guidelines for image use, informed by '{', '.join(image_style_preferences) if image_style_preferences else 'industry best practices and visual style.'}' (e.g., "Use high-quality, professional photos with a focus on people and positive emotions. Apply rounded corners to stand-alone images if '{button_shape}' is rounded.").
    *   "overall_layout_philosophy": Brief text (e.g., "Clean, spacious, and user-centric design with clear visual hierarchy. Prioritize readability and intuitive navigation.").

Example of a section's "content" if content_source is 'provide_later':
"content": {{
  "headline": "Our Core Services",
  "subheadline": "[User to provide a brief overview of their main service categories.]",
  "body_text": "[User to list and describe each core service. Example: Service 1 - [Description], Service 2 - [Description].]",
  "cta_button": {{ "text": "View All Services", "link_suggestion": "/services" }}
}}

Ensure the entire output is a single, valid JSON object without any surrounding text or markdown.
"""

    generation_config = {
        "temperature": 0.5,
        "response_mime_type": "application/json",
    }

    try:
        model_instance = genai.GenerativeModel("gemini-1.5-flash") # Recreate the model just in case, if configure was global
        response = model_instance.generate_content(prompt, generation_config=generation_config)

        # Important: Gemini with response_mime_type="application/json" might return a response,
        # which is already a Python dict if using the latest SDK version,
        # or a string that needs to be parsed. Let's check.
        # According to documentation: response.text should contain a JSON string.
        if hasattr(response, 'text') and isinstance(response.text, str):
            # Attempt to parse for validation before returning
            try:
                json.loads(response.text) # Check if it's valid JSON
                return response.text
            except json.JSONDecodeError as json_err:
                print(f"AI returned a string but it's not valid JSON: {json_err}")
                print(f"Malformed JSON string: {response.text[:500]}...") # Show start of string
                return translator("AI returned malformed JSON. Please try again or adjust the prompt.")
        # If Gemini SDK returned an already parsed dict (unlikely for .text, but possible for .parts)
        # elif isinstance(response.candidates[0].content.parts[0].text, dict): # Example, actual path may differ
        #     return json.dumps(response.candidates[0].content.parts[0].text)

        # If response.text is empty or something went wrong
        error_message = f"Received unexpected response structure from AI. Response text: {getattr(response, 'text', 'N/A')}"
        if response.prompt_feedback:
            error_message += f" Prompt Feedback: {response.prompt_feedback}"
        print(error_message)
        return translator("AI response was not in the expected format. Please try again.")

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        # Additional error information, if any
        error_details = str(e)
        if hasattr(e, 'response') and e.response:
            error_details += f" | API Response Error: {e.response}"
        elif hasattr(e, 'message'):
            error_details += f" | Message: {e.message}"

        # Check for specific Gemini errors (e.g., BLOCK_REASON_SAFETY)
        # if "safety" in error_details.lower(): # Simplified check
        #     return translator("The request was blocked due to safety concerns. Please modify your inputs.")

        return translator(f"Something went wrong with AI generation: {error_details[:100]}... Please try again.")