import re

def to_upper_snake_case(text: str) -> str:
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)

    # Replace spaces with underscores
    text = text.replace(' ', '_')

    # Replace "-" with underscores
    text = text.replace('-', '_')

    # Convert to uppercase
    text = text.upper()

    # Clean up multiple underscores
    text = re.sub(r'_+', '_', text)

    # Remove leading/trailing underscores
    text = text.strip('_')

    return text
