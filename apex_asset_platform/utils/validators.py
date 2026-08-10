
def validate_unique_ids(generated_id, instance_list: list) -> bool:
    for item in instance_list:
        if item.asset_id != generated_id:
            return True
    return False