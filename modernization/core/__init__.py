"""
Core modernization components for VTT system.

This module contains the primary modernization infrastructure components:
- Spec Compliance Module: Ensures adherence to modern spec standards
- Amazon Integration Layer: Provides Amazon development tools integration
- Property Test Framework: Implements property-based testing with Hypothesis
- Modernization Engine: Orchestrates the modernization process
"""

from .spec_compliance import SpecComplianceModule
# from .amazon_integration import AmazonIntegrationLayer  # TODO: Implement in future tasks
# from .property_testing import PropertyTestFramework  # TODO: Fix hypothesis dependency
# from .modernization_engine import ModernizationEngine  # TODO: Implement in future tasks

__all__ = [
    'SpecComplianceModule',
    # 'AmazonIntegrationLayer',
    # 'PropertyTestFramework', 
    # 'ModernizationEngine'
]