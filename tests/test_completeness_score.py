import pytest

from profile_extraction_chatbot.schemas import (
    UserProfile,
    Education,
    ProfessionalExperience,
)
from profile_extraction_chatbot import constants


@pytest.mark.parametrize(
    "user_profile, expected_score",
    [
        (UserProfile.empty_instance(), 0),
        (
            UserProfile(
                name="Alice",
                age=0,
                location="",
                education=Education.empty_instance(),
                professional_experience=[],
            ),
            constants.HIGH_WEIGHT,
        ),
        (
            UserProfile(
                name="Alice",
                age=30,
                location="",
                education=Education.empty_instance(),
                professional_experience=[],
            ),
            constants.HIGH_WEIGHT + constants.LOW_WEIGHT,
        ),
        (
            UserProfile(
                name="Alice",
                age=30,
                location="Romania",
                education=Education.empty_instance(),
                professional_experience=[],
            ),
            constants.HIGH_WEIGHT + constants.LOW_WEIGHT + constants.MEDIUM_WEIGHT,
        ),
        (
            UserProfile(
                name="Alice",
                age=30,
                location="Romania",
                education=Education(
                    degree="BSc", institution="Oxford", graduation_year=2010
                ),
                professional_experience=[],
            ),
            constants.HIGH_WEIGHT
            + constants.LOW_WEIGHT
            + constants.MEDIUM_WEIGHT
            + constants.MEDIUM_WEIGHT,
        ),
        (
            UserProfile(
                name="Alice",
                age=30,
                location="Romania",
                education=Education(
                    degree="BSc", institution="Oxford", graduation_year=2010
                ),
                professional_experience=[
                    ProfessionalExperience(
                        title="Software Engineer",
                        company="Google",
                        duration="5 years",
                        projects="AI Chatbot",
                    )
                ],
            ),
            constants.HIGH_WEIGHT
            + constants.LOW_WEIGHT
            + constants.MEDIUM_WEIGHT
            + constants.MEDIUM_WEIGHT
            + constants.MEDIUM_WEIGHT,
        ),
    ],
)
def test_completeness_score(user_profile, expected_score):
    assert user_profile.compute_completeness_score() == expected_score
