from __future__ import annotations

from pydantic import BaseModel

from profile_extraction_chatbot import constants


class UserProfile(BaseModel):
    """The user profile schema, which includes fields for the user's name, age, location, education,
    and professional experiences."""

    """The user's full name."""
    name: str

    """The user's age."""
    age: int

    """The user's location (city, country)."""
    location: str

    """Key details about the user's educational background, including degrees, institutions, and graduation years."""
    education: Education

    """Each entity should represent a job role, including fields like title, company, duration,
     and notable projects or responsibilities."""
    professional_experience: list[ProfessionalExperience]

    def compute_completeness_score(self) -> int:
        """Compute the profile completeness score based on the presence of required fields."""

        return sum(
            [
                self.name_weight(),
                self.location_weight(),
                self.professional_experience_weight(),
                self.education_weight(),
                self.age_weight(),
            ]
        )

    def name_weight(self) -> int:
        """Compute the weight of the user's name in the profile completeness score."""

        if self.name:
            return constants.HIGH_WEIGHT

        return constants.DEFAULT_WEIGHT

    def location_weight(self) -> int:
        """Compute the weight of the user's location in the profile completeness score."""

        if self.location:
            return constants.MEDIUM_WEIGHT

        return constants.DEFAULT_WEIGHT

    def professional_experience_weight(self) -> int:
        """Compute the weight of the user's professional experiences in the profile completeness score."""

        return len(self.professional_experience) * constants.MEDIUM_WEIGHT

    def education_weight(self) -> int:
        """Compute the weight of the user's education in the profile completeness score."""

        if not self.education.is_empty():
            return constants.MEDIUM_WEIGHT

        return constants.DEFAULT_WEIGHT

    def age_weight(self) -> int:
        """Compute the weight of the user's age in the profile completeness score."""

        if self.age:
            return constants.LOW_WEIGHT

        return constants.DEFAULT_WEIGHT

    def __str__(self) -> str:
        return (
            f"Name: {self.name}, Age: {self.age}, Location: {self.location}, "
            f"Education: {self.education}, Professional Experience: {self.professional_experience}"
        )

    @classmethod
    def empty_instance(cls):
        return cls(
            name="",
            age=0,
            location="",
            education=Education(degree="", institution="", graduation_year=0),
            professional_experience=[],
        )


class Education(BaseModel):
    """The user's educational background, including fields for degree, institution, and graduation year."""

    """The user's degree."""
    degree: str

    """The institution where the user studied."""
    institution: str

    """The year the user graduated."""
    graduation_year: int

    def is_empty(self) -> bool:
        """Check if the education instance is empty (all fields are empty)."""

        return not any((self.degree, self.institution, self.graduation_year))

    def __str__(self) -> str:
        return f"Degree: {self.degree}, Institution: {self.institution}, Graduation Year: {self.graduation_year}"


class ProfessionalExperience(BaseModel):
    """The user's professional experience, including fields for job title, company, duration,
    and key projects or responsibilities.
    """

    """The user's job title."""
    title: str

    """The company where the user worked."""
    company: str

    """The duration of the user's employment."""
    duration: str

    """Key projects or responsibilities the user had in this role."""
    projects: str

    def __str__(self) -> str:
        return f"Title: {self.title}, Company: {self.company}, Duration: {self.duration}, Projects: {self.projects}"
