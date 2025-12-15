

def custom_preprocessing_hook(endpoints):
    excluded_paths = [
        '/api/user/',
        '/api/user/resend_activation/',
        '/api/user/reset_phone_number/',
        '/api/user/reset_phone_number_confirm/',
        '/api/user/reset_password/',
        '/api/user/reset_password_confirm/',
        '/api/user/set_password/',
        '/api/user/set_phone_number/',
        '/api/user/activation/',
    ]

    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        if path not in excluded_paths:
            filtered.append((path, path_regex, method, callback))

    return filtered