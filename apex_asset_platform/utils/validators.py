def validate_unique_ids(generated_id: str, instance_list: list) -> bool:
    """Checks whether a generated ID tag is unique across domain object lists.

    Args:
        generated_id (str): Generated ID string to check.
        instance_list (list): List of domain objects (Equipment or Customer).

    Returns:
        bool: True if generated_id is unique (not found in list), False otherwise.
    """
    for item in instance_list:
        item_id = getattr(item, "customer_id", getattr(item, "asset_id", None))
        if item_id == generated_id:
            return False
    return True


def gmail_validator(email: str) -> bool:
    """Validates if an email address is a valid @gmail.com account.

    Args:
        email (str): Email string to validate.

    Returns:
        bool: True if email ends with '@gmail.com', False otherwise.
    """
    if not isinstance(email, str):
        return False
    return email.strip().lower().endswith("@gmail.com")


def phone_validator(phone: str) -> bool:
    """Validates if a phone number starts with '09' and is exactly 11 digits long.

    Args:
        phone (str): Phone number string to validate.

    Returns:
        bool: True if phone number starts with '09' and has 11 digits, False otherwise.
    """
    if not isinstance(phone, str):
        return False
    clean_phone = phone.strip()
    return clean_phone.startswith("09") and len(clean_phone) == 11 and clean_phone.isdigit()