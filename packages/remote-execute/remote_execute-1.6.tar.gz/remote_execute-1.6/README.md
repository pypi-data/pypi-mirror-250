# remote-execute
Execute remote code fetched from a URL

## Example 1:
```
remote_code_urls = [
    'https://example.com/code1.py',
    'https://example.com/code2.py',
    'https://example.com/code3.py',
]

execute_remote_code(remote_code_urls)
```

## Example 2:
```
remote_code_urls = [
    'https://example.com/code1.py',
    'https://example.com/code2.py',
    'https://example.com/code3.py',
]
auth_tokens = [
    'your_auth_token_1',
    None, # No token for the 2nd URL
    'your_auth_token_3',
]
user_agents = [
    'your_user_agent_1',
    'your_user_agent_2',
    None, # No user agent for the 3rd URL
]

execute_remote_code(remote_code_urls, auth_tokens, user_agents)
```