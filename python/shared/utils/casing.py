def camel_to_snake(camel):
    # Convert camelCase to snake_case
    return ''.join(['_' + char.lower() if char.isupper() else char for char in camel]).lstrip('_')
