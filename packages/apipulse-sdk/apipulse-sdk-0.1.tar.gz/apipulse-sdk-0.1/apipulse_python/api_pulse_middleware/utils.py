import pprint
import re

def simplify_regex_pattern(pattern: str) -> str:
    # Remove start (^) and end ($ or \\Z) of string regex symbols
    pattern = pattern.replace('^', '').replace('$', '').replace('\\Z', '')

    # Replace named regex groups with a more readable format using {}
    pattern = re.sub(r'\(\?P<(\w+)>[^)]+\)', r'{\1}', pattern)

    # Replace unnamed URL parameters (e.g., (\d+)) with a generic placeholder
    pattern = re.sub(r'\([^\)]*\)', '{param}', pattern)

    # Simplify common regex patterns
    pattern = pattern.replace('\\.', '.').replace('\\-', '-').replace('\\/', '/')

    # Handle optional parts in the URL
    pattern = pattern.replace('/?', '/')

    # Additional simplifications can be added here

    return pattern



def test():
    pattern1 = '^admin/^auth/user/^(?P<object_id>.+)/change/\\Z'
    print(simplify_regex_pattern(pattern1))
    
    pattern2 = '^browser/^number/(?P<number>[0-9]+)/\\Z'
    print(simplify_regex_pattern(pattern2))

if __name__=='__main__':
    # Example usage
    test()
