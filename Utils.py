

def get_login_info(filepath='./redditLogin'):
    """
    Acquires Reddit app login information from txt file.
    Assumes the first 5 lines contain:
        - Client ID,
        - Client Secret,
        - User Agent,
        - Username
        - Password
    :param filepath: Path to txt file containing Reddit app login information.
    :return: return dictionary containing login information
    """
    # Acquires login information from text file.
    with open(filepath, 'r') as fp:
        client_id = fp.readline().strip()
        client_secret = fp.readline().strip()
        user_agent = fp.readline().strip()
        username = fp.readline().strip()
        password = fp.readline().strip()

    # Return login information as dictionary.
    login_info = {'client_id': client_id,
                  'client_secret': client_secret,
                  'user_agent': user_agent,
                  'username': username,
                  'password': password}
    return login_info






