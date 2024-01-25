from fastapi import HTTPException


def get_person_or_404(person):
    if person is None:
        raise HTTPException(status_code=404, detail="User not found")
    return person
