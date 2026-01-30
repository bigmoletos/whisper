"""
Property models for VTT modernization testing.

This module defines property types and validation criteria for
property-based testing of VTT components.
"""

import logging
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import time

logger = logging.getLogger(__name__)


class PropertyType(Enum):
    """Types of properties for testing."""
    ROUND_TRIP = "round_trip"
    INVARIANT = "invariant"
    METAMORPHIC = "metamorphic"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE = "performance"
    SECURITY = "security"


class ValidationCriteriaType(Enum):
    """Types of validation criteria."""
    BOOLEAN = "boolean"
    NUMERIC_RANGE = "numeric_range"
    STRING_PATTERN = "string_pattern"
    COLLECTION_SIZE = "collection_size"
    CUSTOM_FUNCTION = "custom_function"


@dataclass
class ValidationCriteria:
    """Validation criteria for property testing."""
    criteria_type: ValidationCriteriaType
    expected_value: Any = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    validator_function: Optional[Callable] = None
    error_message: str = "Validation failed"
    
    def validate(self) -> List[str]:
        """Validate the validation criteria configuration."""
        errors = []
        
        if not isinstance(self.criteria_type, ValidationCriteriaType):
            errors.append("ValidationCriteria.criteria_type must be ValidationCriteriaType enum")
        
        if self.criteria_type == ValidationCriteriaType.NUMERIC_RANGE:
            if self.min_value is None and self.max_value is None:
                errors.append("NUMERIC_RANGE criteria requires min_value or max_value")
            if (self.min_value is not None and self.max_value is not None 
                and self.min_value > self.max_value):
                errors.append("min_value must be <= max_value for NUMERIC_RANGE")
        
        if self.criteria_type == ValidationCriteriaType.STRING_PATTERN:
            if not self.pattern:
                errors.append("STRING_PATTERN criteria requires pattern")
        
        if self.criteria_type == ValidationCriteriaType.CUSTOM_FUNCTION:
            if not callable(self.validator_function):
                errors.append("CUSTOM_FUNCTION criteria requires callable validator_function")
        
        if not isinstance(self.error_message, str):
            errors.append("ValidationCriteria.error_message must be string")
        
        return errors
    
    def check_value(self, value: Any) -> bool:
        """
        Check if a value meets the validation criteria.
        
        Args:
            value: Value to validate
            
        Returns:
            True if value meets criteria
        """
        try:
            if self.criteria_type == ValidationCriteriaType.BOOLEAN:
                return bool(value) == bool(self.expected_value)
            
            elif self.criteria_type == ValidationCriteriaType.NUMERIC_RANGE:
                if not isinstance(value, (int, float)):
                    return False
                
                if self.min_value is not None and value < self.min_value:
                    return False
                if self.max_value is not None and value > self.max_value:
                    return False
                return True
            
            elif self.criteria_type == ValidationCriteriaType.STRING_PATTERN:
                if not isinstance(value, str):
                    return False
                import re
                return bool(re.match(self.pattern, value))
            
            elif self.criteria_type == ValidationCriteriaType.COLLECTION_SIZE:
                if not hasattr(value, '__len__'):
                    return False
                size = len(value)
                if self.min_value is not None and size < self.min_value:
                    return False
                if self.max_value is not None and size > self.max_value:
                    return False
                return True
            
            elif self.criteria_type == ValidationCriteriaType.CUSTOM_FUNCTION:
                if self.validator_function:
                    return bool(self.validator_function(value))
                return False
            
            else:
                return value == self.expected_value
                
        except Exception as e:
            logger.error(f"Error checking validation criteria: {e}", exc_info=True)
            return False


@dataclass
class PropertyTestResult:
    """Result of a property test execution."""
    property_name: str
    success: bool
    execution_time: float
    iterations_run: int
    counterexample: Optional[Any] = None
    error_message: Optional[str] = None
    validation_details: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate property test result."""
        errors = []
        
        if not isinstance(self.property_name, str):
            errors.append("PropertyTestResult.property_name must be string")
        
        if not isinstance(self.success, bool):
            errors.append("PropertyTestResult.success must be boolean")
        
        if not isinstance(self.execution_time, (int, float)) or self.execution_time < 0:
            errors.append("PropertyTestResult.execution_time must be non-negative number")
        
        if not isinstance(self.iterations_run, int) or self.iterations_run < 0:
            errors.append("PropertyTestResult.iterations_run must be non-negative integer")
        
        if self.error_message is not None and not isinstance(self.error_message, str):
            errors.append("PropertyTestResult.error_message must be string or None")
        
        if not isinstance(self.validation_details, dict):
            errors.append("PropertyTestResult.validation_details must be dictionary")
        
        return errors


@dataclass
class TranscriptionProperty:
    """Definition of a transcription property for testing."""
    name: str
    description: str
    property_type: PropertyType
    test_function: Callable
    requirements_reference: str
    validation_criteria: ValidationCriteria
    priority: int = 1  # 1=high, 2=medium, 3=low
    enabled: bool = True
    timeout_seconds: float = 30.0
    max_iterations: int = 100
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate transcription property definition."""
        errors = []
        
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("TranscriptionProperty.name must be non-empty string")
        
        if not isinstance(self.description, str):
            errors.append("TranscriptionProperty.description must be string")
        
        if not isinstance(self.property_type, PropertyType):
            errors.append("TranscriptionProperty.property_type must be PropertyType enum")
        
        if not callable(self.test_function):
            errors.append("TranscriptionProperty.test_function must be callable")
        
        if not isinstance(self.requirements_reference, str):
            errors.append("TranscriptionProperty.requirements_reference must be string")
        
        if self.priority not in [1, 2, 3]:
            errors.append("TranscriptionProperty.priority must be 1, 2, or 3")
        
        if not isinstance(self.enabled, bool):
            errors.append("TranscriptionProperty.enabled must be boolean")
        
        if not isinstance(self.timeout_seconds, (int, float)) or self.timeout_seconds <= 0:
            errors.append("TranscriptionProperty.timeout_seconds must be positive number")
        
        if not isinstance(self.max_iterations, int) or self.max_iterations <= 0:
            errors.append("TranscriptionProperty.max_iterations must be positive integer")
        
        if not isinstance(self.tags, list):
            errors.append("TranscriptionProperty.tags must be list")
        elif not all(isinstance(tag, str) for tag in self.tags):
            errors.append("TranscriptionProperty.tags must contain only strings")
        
        if not isinstance(self.dependencies, list):
            errors.append("TranscriptionProperty.dependencies must be list")
        elif not all(isinstance(dep, str) for dep in self.dependencies):
            errors.append("TranscriptionProperty.dependencies must contain only strings")
        
        # Validate nested validation criteria
        errors.extend(self.validation_criteria.validate())
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if property definition is valid."""
        return len(self.validate()) == 0
    
    def can_run(self, available_properties: List[str]) -> bool:
        """
        Check if property can run based on dependencies.
        
        Args:
            available_properties: List of available property names
            
        Returns:
            True if all dependencies are available
        """
        if not self.enabled:
            return False
        
        return all(dep in available_properties for dep in self.dependencies)
    
    def execute(self, test_context: Dict[str, Any]) -> PropertyTestResult:
        """
        Execute the property test.
        
        Args:
            test_context: Context for test execution
            
        Returns:
            PropertyTestResult with execution results
        """
        start_time = time.time()
        
        try:
            # Execute the test function
            result = self.test_function(test_context)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Validate result against criteria
            validation_success = self.validation_criteria.check_value(result)
            
            return PropertyTestResult(
                property_name=self.name,
                success=validation_success,
                execution_time=execution_time,
                iterations_run=test_context.get('iterations', 1),
                validation_details={
                    'result': result,
                    'criteria_type': self.validation_criteria.criteria_type.value,
                    'expected': self.validation_criteria.expected_value
                }
            )
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.error(f"Property test {self.name} failed: {e}", exc_info=True)
            
            return PropertyTestResult(
                property_name=self.name,
                success=False,
                execution_time=execution_time,
                iterations_run=0,
                error_message=str(e),
                validation_details={'exception': str(e)}
            )
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get property metadata for reporting."""
        return {
            'name': self.name,
            'description': self.description,
            'type': self.property_type.value,
            'requirements_ref': self.requirements_reference,
            'priority': self.priority,
            'enabled': self.enabled,
            'tags': self.tags,
            'dependencies': self.dependencies,
            'timeout': self.timeout_seconds,
            'max_iterations': self.max_iterations
        }


@dataclass
class PropertySuite:
    """Collection of related properties for testing."""
    name: str
    description: str
    properties: List[TranscriptionProperty]
    setup_function: Optional[Callable] = None
    teardown_function: Optional[Callable] = None
    parallel_execution: bool = False
    
    def validate(self) -> List[str]:
        """Validate property suite."""
        errors = []
        
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("PropertySuite.name must be non-empty string")
        
        if not isinstance(self.description, str):
            errors.append("PropertySuite.description must be string")
        
        if not isinstance(self.properties, list):
            errors.append("PropertySuite.properties must be list")
        elif not all(isinstance(prop, TranscriptionProperty) for prop in self.properties):
            errors.append("PropertySuite.properties must contain only TranscriptionProperty objects")
        
        if self.setup_function is not None and not callable(self.setup_function):
            errors.append("PropertySuite.setup_function must be callable or None")
        
        if self.teardown_function is not None and not callable(self.teardown_function):
            errors.append("PropertySuite.teardown_function must be callable or None")
        
        if not isinstance(self.parallel_execution, bool):
            errors.append("PropertySuite.parallel_execution must be boolean")
        
        # Validate all properties
        for i, prop in enumerate(self.properties):
            prop_errors = prop.validate()
            for error in prop_errors:
                errors.append(f"Property {i} ({prop.name}): {error}")
        
        # Check for duplicate property names
        property_names = [prop.name for prop in self.properties]
        if len(property_names) != len(set(property_names)):
            errors.append("PropertySuite contains duplicate property names")
        
        return errors
    
    def get_enabled_properties(self) -> List[TranscriptionProperty]:
        """Get list of enabled properties."""
        return [prop for prop in self.properties if prop.enabled]
    
    def get_properties_by_priority(self, priority: int) -> List[TranscriptionProperty]:
        """Get properties by priority level."""
        return [prop for prop in self.properties if prop.priority == priority and prop.enabled]
    
    def get_properties_by_type(self, property_type: PropertyType) -> List[TranscriptionProperty]:
        """Get properties by type."""
        return [prop for prop in self.properties if prop.property_type == property_type and prop.enabled]
    
    def resolve_dependencies(self) -> List[TranscriptionProperty]:
        """
        Resolve property dependencies and return execution order.
        
        Returns:
            List of properties in dependency-resolved order
        """
        enabled_props = self.get_enabled_properties()
        property_names = {prop.name for prop in enabled_props}
        
        # Simple topological sort for dependency resolution
        resolved = []
        remaining = enabled_props.copy()
        
        while remaining:
            # Find properties with no unresolved dependencies
            ready = []
            for prop in remaining:
                if prop.can_run([p.name for p in resolved]):
                    ready.append(prop)
            
            if not ready:
                # Circular dependency or missing dependency
                logger.warning(f"Cannot resolve dependencies for properties: {[p.name for p in remaining]}")
                # Add remaining properties anyway
                resolved.extend(remaining)
                break
            
            # Add ready properties to resolved list
            resolved.extend(ready)
            for prop in ready:
                remaining.remove(prop)
        
        return resolved
    
    def execute_suite(self, test_context: Dict[str, Any]) -> List[PropertyTestResult]:
        """
        Execute all properties in the suite.
        
        Args:
            test_context: Context for test execution
            
        Returns:
            List of PropertyTestResult objects
        """
        results = []
        
        try:
            # Setup
            if self.setup_function:
                self.setup_function(test_context)
            
            # Get execution order
            execution_order = self.resolve_dependencies()
            
            # Execute properties
            for prop in execution_order:
                logger.info(f"Executing property: {prop.name}")
                result = prop.execute(test_context)
                results.append(result)
                
                # Stop on critical failures if needed
                if not result.success and prop.priority == 1:
                    logger.warning(f"Critical property {prop.name} failed, continuing with remaining tests")
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing property suite {self.name}: {e}", exc_info=True)
            return results
            
        finally:
            # Teardown
            try:
                if self.teardown_function:
                    self.teardown_function(test_context)
            except Exception as e:
                logger.error(f"Error in suite teardown: {e}", exc_info=True)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get suite summary information."""
        enabled_props = self.get_enabled_properties()
        
        return {
            'name': self.name,
            'description': self.description,
            'total_properties': len(self.properties),
            'enabled_properties': len(enabled_props),
            'property_types': {
                ptype.value: len(self.get_properties_by_type(ptype))
                for ptype in PropertyType
            },
            'priority_distribution': {
                f'priority_{i}': len(self.get_properties_by_priority(i))
                for i in [1, 2, 3]
            },
            'parallel_execution': self.parallel_execution
        }