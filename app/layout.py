      
import streamlit as st

def show_form(_):
    st.subheader(_("Enter Website Details"))

    # --- Basic Information ---
    company_name = st.text_input(_("Company or Project Name"), key="company_name")
    industry_options = ["Tech", "Education", "Finance", "Healthcare", "Fashion", "Restaurant", "Travel", "Personal Blog", "E-commerce", "Non-profit", "Other"]
    industry = st.selectbox(_("Select Industry"), industry_options, key="industry")

    # --- Content ---
    st.markdown("---")
    st.markdown(f"##### {_('Content Strategy')}")
    content_source = st.radio(
        _("Do you have existing content (text, PDF, link)?"),
        [_("No, please generate content"), _("Yes, I will provide content later (AI will generate placeholders)")], # Option "Yes, I have content" simplified for now
        key="content_source"
    )
    # In the future, could add st.file_uploader or st.text_area if "Yes"

    has_no_description = st.checkbox(_("I have no specific project description, suggest based on industry and style"), key="has_no_description")

    if not has_no_description:
        description = st.text_area(_("Describe your company/project/service or goal"), key="description")
    else:
        description = ""

    # --- Branding and Design ---
    st.markdown("---")
    st.markdown(f"##### {_('Branding & Design Preferences')}")
    generate_logo = st.checkbox(_("Do you want AI to suggest a concept for a logo?"), value=True, key="generate_logo")
    has_brand_book = st.checkbox(_("Do you have an existing brand book/style guide?"), key="has_brand_book")
    # If has_brand_book, in the future could add field for upload or description

    visual_style_options = ["Modern", "Minimalist", "Friendly", "Playful", "Corporate", "Elegant", "Bold", "Techy"]
    visual_style = st.selectbox(_("Choose a general visual style"), visual_style_options, key="visual_style")

    # --- Website Structure ---
    st.markdown("---")
    st.markdown(f"##### {_('Website Structure')}")
    let_ai_decide_pages = st.checkbox(_("Let AI decide the number of pages"), value=False, key="let_ai_decide_pages")

    if let_ai_decide_pages:
        num_pages_display = _("AI will decide")
        num_pages_value = "AI_DECIDES" # special value for AI
        st.info(f"{_('Number of pages')}: {num_pages_display}")
    else:
        num_pages_value = st.slider(_("How many pages do you want?"), 1, 10, 3, key="num_pages_slider")
        num_pages_display = str(num_pages_value)


    # --- Style Elements ---
    # color_theme removed, as AI will generate a palette based on industry/style
    # Can keep "preferred primary color" if needed, but for MVP it's better to let AI decide
    # preferred_primary_color = st.color_picker(_("Pick a preferred primary color (optional)"), "#2272FF", key="preferred_primary_color")

    icon_style_options = ["Flat", "Outline", "Glyph", "3D-like (subtle)", "Abstract"]
    icon_style = st.selectbox(_("Choose icon style"), icon_style_options, key="icon_style")
    button_shape_options = ["Rounded", "Slightly Rounded", "Square", "Pill Shaped"]
    button_shape = st.radio(_("Button Shape"), button_shape_options, key="button_shape")
    image_style = st.multiselect(
        _("Preferred image characteristics (optional)"),
        ["Illustrations", "Photographs", "Abstract", "Bright", "Muted", "With text overlay", "Rounded corners", "Full-width"],
        key="image_style"
    )


    # Validation and data collection
    if company_name.strip(): # Ensure company name is not empty
        user_data = {
            "company_name": company_name,
            "industry": industry,
            "content_source": "generate" if content_source == _("No, please generate content") else "provide_later",
            "description": description if not has_no_description else "", # Pass empty if "has_no_description" is checked
            "ai_should_suggest_description": has_no_description,
            "generate_logo_concept": generate_logo,
            "has_brand_book": has_brand_book,
            "visual_style": visual_style,
            "num_pages": num_pages_value, # will be either a number or "AI_DECIDES"
            "icon_style": icon_style,
            "button_shape": button_shape,
            "image_style_preferences": image_style,
            # "preferred_primary_color": preferred_primary_color # if uncommented above
        }
        return user_data
    else:
        # Could show a warning if company name is empty on attempt to submit
        # But Streamlit usually handles this itself (button might be inactive or nothing happens)
        return None

    