# Python guidelines
- Keep code readable.
- Prefer pythonic best practices (list comprehensions instead of loops).
- Use lines of around 100 characters
- before every new step of a function add a line of comment for explanation.
- In a function try to not define many variables but use return statements directly when possible.
- Do not repeat yourself, write modular code and use decorators
- Define classes only when necessary
- Variables should have lower snake case naming convention
- Docstrings should have the following format:
    - Description.
    - Args:
        - arg_1: description
        - arg_2: description
    - Returns: description
    - Notes:
        - note_1
        - note_2
- for type hinting, avoid using typing package except for the type "Any"

# JSON guidelines
- Use maximum indentation, I like to have readable files
- use self-explanatory keys
- use lower snake case naming for the keys in json files