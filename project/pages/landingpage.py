import reflex as rx

def landing():
    # Create a custom style directly on the root element to ensure full coverage
    app_style = {
        "min_height": "100vh",
        "min_width": "100vw",
        "margin": "0px",
        "padding": "0px",
        "background": "linear-gradient(to bottom, #d3edf8, #5393c8)",
        "overflow": "hidden",  # Prevent scrolling
        "position": "absolute",
        "top": "0px",
        "left": "0px",
        "right": "0px",
        "bottom": "0px",
    }
    
    # Wave shape at the bottom
    wave_style = {
        "position": "absolute",
        "bottom": "0",
        "left": "0",
        "width": "100%",
        "height": "150px",
        "background": "white",
        "border_radius": "100% 100% 0 0",
        "transform": "scale(1.5, 1)",
        "z_index": "1",
    }
    
    # White area below the wave
    bottom_white_style = {
        "position": "absolute",
        "bottom": "0",  # Ensure it sticks to the bottom
        "left": "0",
        "width": "100%",
        "height": "100px",  # Height of the white area below the wave
        "background": "white",
        "z_index": "0",
    }
    
    # Large text style (heading)
    large_text_style = {
        "font_size": "48px",  # Larger font size for the main heading
        "font_weight": "medium",
        "margin_bottom": "8",
        "color": "#2c6283",  # Custom color for the text
    }
    
    # Smaller text style (subheading or paragraph)
    small_text_style = {
        "font_size": "20px",  # Smaller font size for the subheading
        "color": "#346579",  # Custom color for the text
        "max_width": "500px",  # Optional: restrict width for better formatting
        "padding_top": "15px",
    }
    
    # Text content style
    text_content_style = {
        "position": "absolute",
        "top": "30%",
        "left": "10%",
        "z_index": "2",
    }
    
    # Graduation cap icon style - moved higher
    hat_icon_style = {
        "position": "absolute",
        "top": "5%",  # Changed from 20% to 10% to move it higher
        "right": "10%",
        "z_index": "3",
        "width": "750px",
        "height": "750px",
        "object_fit": "contain",
    }
    
    return rx.fragment(
        # Add some global styles first to ensure body/html have no margins
        rx.script("document.body.style.margin = '0'; document.body.style.padding = '0'; document.documentElement.style.margin = '0'; document.documentElement.style.padding = '0';"),
        
        rx.box(
            # Text content
            rx.box(
                rx.heading(
                    "Welcome to StudySphere!",
                    **large_text_style  # Apply large text style
                ),
                rx.text(
                    "Your classroom, simplified and connected - start your academic adventure with us!",
                    **small_text_style  # Apply smaller text style
                ),
                **text_content_style
            ),
            
            # Graduation cap icon
            rx.image(
                src="/logo.png",  # Changed back to hat_icon.png from logo.png
                **hat_icon_style
            ),
            
            # Wave shape at the bottom
            rx.box(
                **wave_style
            ),
            
            # White area below the wave
            rx.box(
                **bottom_white_style
            ),

            rx.box(
                rx.button(
                    "Get Started",
                    on_click=rx.redirect("/login"),
                    bg="#5996af",
                    color="white",
                    width="200px",     # Add button width
                    height="60px",     # Add button height
                    padding="20px",    # Add padding
                    font_size="20px"   # Add font size
                ),
                text_align="center", 
                position="absolute",
                top="55%",
                left="25%",
                transform="translate(-50%, -50%)",
                padding="4",
                bg="rgba(255, 255, 255, 0.8)"
            ),

            # Apply the full background style
            **app_style
        )
    )
