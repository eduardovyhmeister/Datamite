"""Enumerations used in choices for some DB fields."""


from django.db import models


class CriterionOption(models.TextChoices):
    """The possible options for Criterion."""
    COST_AND_COST_REDUCTION = "COST_AND_COST_REDUCTION", "Cost and Cost Reduction"
    PRODUCTIVITY_INCREASE = "PRODUCTIVITY_INCREASE", "Productivity Increase"
    QUALITY_AND_DATA_INCREASE = "QUALITY_AND_DATA_INCREASE", "Quality and Data Increase"
    SAFETY_INCREASE = "SAFETY_INCREASE", "Safety Increase"
    LEARNING_AND_GROWTH_INCREASE = "LEARNING_AND_GROWTH_INCREASE", "Learning and Growth Increase"
    USER_SATISFACTION = "USER_SATISFACTION", "User Satisfaction"
    
    
class BSCFamily(models.TextChoices):
    """The possible choices for the BSC family (for KPIs)."""
    CUSTOMER = "CUSTOMER", "Customer"
    FINANCIAL = "FINANCIAL", "Financial"
    EDUCATION_AND_GROWTH = "EDUCATION AND GROWTH", "Education and Growth"
    INTERNAL_PROCESSES = "INTERNAL PROCESSES", "Internal Processes"
        

class UserType(models.TextChoices):
    """The possible types of datamite users (for Evaluation)."""
    SERVICE_USER = "SERVICE_USER", "Service User"
    DATA_PROVIDER = "DATA_PROVIDER", "Data Provider"
    SERVICE_STAKEHOLDER = "SERVICE_STAKEHOLDER", "Service Stakeholder"


class UserDomain(models.TextChoices):
    """The possible expertise domains of a user."""
    MANUFACTURING = "MANUFACTURING", "Manufacturing"
    AEROSPACE = "AEROSPACE", "Aerospace"
    COMMUNICATIONS = "COMMUNICATIONS", "Communications"
    CHEMICAL_AND_PHARMACEUTICAL = "CHEMICAL_AND_PHARMACEUTICAL", "Chemical and Pharmaceutical"
    CONSUMER_GOODS_AND_RETAIL = "CONSUMER_GOODS_AND_RETAIL", "Consumer, Goods, and Retail"
    ENERGY_AND_UTILITIES = "ENERGY_AND_UTILITIES", "Energy and Utilities"
    FINANCIAL_SERVICES = "FINANCIAL_SERVICES", "Financial Services"
    FREIGHT_LOGISTICS_AND_TRANSPORTATION = "FREIGHT_LOGISTICS_AND_TRANSPORTATION", "Freight, Logistics, and Transportations"
    HEALTH_AND_LIFE_SCIENCES = "HEALTH_AND_LIFE_SCIENCES", "Health and Life Sciences"
    HOSPITALITY_AND_TRAVEL = "HOSPITALITY_AND_TRAVEL", "Hospitality and Travel"
    MEDIA_ENTERTAINMENT_AND_PUBLISHING = "MEDIA_ENTERTAINMENT_AND_PUBLISHING", "Media, Entertainment, and Publishing"
    RD_AND_EDUCATION = "RD_AND_EDUCATION", "R&D and Education"
