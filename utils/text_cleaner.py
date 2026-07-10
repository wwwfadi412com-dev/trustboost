import re


def clean_input_text(text: str) -> str:
    """تنظيف النص المدخل من المسافات الزائدة والرموز الغريبة."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text: str, max_length: int = 15000) -> str:
    """تقصير النص ليتوافق مع حدود الـ API وتقليل التكلفة."""
    if len(text) > max_length:
        return text[:max_length] + "... [Text truncated for processing]"
    return text
