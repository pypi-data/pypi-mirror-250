import spin_sdk.wit.imports.variables as spin_variables

def get(key: str) -> str:
    return spin_variables.get(key)