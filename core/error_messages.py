# 00000-09999 # User
# 10000-19999 # Tutor
# 20000-29999 # Pet
# 30000-39999 # Tag
# 40000-49999
# 50000-59999
# 60000-69999
# 70000-79999
# 80000-89999
# 90000-99999
# 450000-459999

# 10000 -> Tutor Does not exist

# 30000 -> Tag already Registered

"""
    70000 -> contact success
    70001 -> 
    70002 -> validation
    70003 -> 
    70004 -> not found
    70005 -> deleted
"""

UserErrorMessage = {
    "not_found": {
        "error": "00004",
        "detail": "User not found",
    },
    "unauthorized": {
        "error": "00001",
        "detail": "Unauthorized",
    },
}

PetErrorMessage = {
    "not_found": {
        "error": "20004",
        "detail": "Pet not found",
    },
    "validation_error": {
        "error": "20002",
        "detail": "Pet validation error"
    },
    "deleted": {
        "error": "20005",
        "detail": "Pet deleted",
    },
    
}


TagErrorMessage = {
    "not_found": {
        "error": "30004",
        "detail": "Invalid tag or pet not found",
    },
    "validation_error": {
        "error": "30002",
        "detail": "Tag validation error"
    },
    "deleted": {
        "error": "30005",
        "detail": "Tag deleted",
    },
    "already_registered": {
        "detail": "Code already Registered.",
        "error": "30007"
    }
}


TutorErrorMessage = {
    "not_found": {
        "error": "10004",
        "detail": "Tutor not found",
    },
    "validation_error": {
        "error": "10002",
        "detail": "Tutor validation error"
    },
    "deleted": {
        "error": "10005",
        "detail": "Tutor deleted",
    },
    "not_tutor_error": {
        "error": "10012",
        "detail": "You're not the tutor of this pet",
    },
    "already_tutor_error": {
        "error": "10013",
        "detail": "You're already the tutor of this pet",
    }
}


ContactErrorMessage = {
    "not_found": {        
        "error": "70004",
        "detail": "Contact not found",
    },
    "validation_error": {
        "error": "70002",
        "detail": "Contact validation error"
    },
    "deleted": {
        "error": "70005",
        "detail": "Contact deleted",
    }
}
