"""
Models package for Gas Station Recommendation App
"""

from .schema import (
    UserPreferences,
    Location,
    GasStation,
    RecommendationRequest,
    RecommendationResponse
)

__all__ = [
    'UserPreferences',
    'Location', 
    'GasStation',
    'RecommendationRequest',
    'RecommendationResponse'
] 