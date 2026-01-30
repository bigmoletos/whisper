"""
Unit tests for EARS pattern validation with various input formats.

Tests comprehensive EARS (Easy Approach to Requirements Syntax) pattern
validation including all pattern types and edge cases.
"""

import pytest
from ..core.spec_compliance import SpecComplianceModule, EARSPattern


class TestEARSPatternValidation:
    """Comprehensive tests for EARS pattern validation."""
    
    @pytest.fixture
    def spec_module(self):
        """Create SpecComplianceModule instance for testing."""
        return SpecComplianceModule()
    
    # Ubiquitous Requirements (THE system SHALL...)
    @pytest.mark.parametrize("requirement,expected", [
        ("THE VTT_System SHALL process audio files", True),
        ("THE VTT_System SHALL transcribe speech to text", True),
        ("THE system SHALL validate user input", True),
        ("THE application SHALL save user preferences", True),
        ("THE VTT_System SHALL support multiple audio formats", True),
        ("THE component SHALL handle errors gracefully", True),
        ("THE module SHALL log all operations", True),
        ("THE service SHALL authenticate users", True),
        ("THE interface SHALL display results", True),
        ("THE database SHALL store transcriptions", True),
    ])
    def test_ubiquitous_pattern_validation(self, spec_module, requirement, expected):
        """Test ubiquitous EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if expected:
            # Verify pattern type detection
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.UBIQUITOUS
    
    # Event-driven Requirements (WHEN ... THE system SHALL...)
    @pytest.mark.parametrize("requirement,expected", [
        ("WHEN user clicks record button, THE VTT_System SHALL start audio capture", True),
        ("WHEN audio file is selected, THE system SHALL begin transcription", True),
        ("WHEN transcription completes, THE application SHALL display results", True),
        ("WHEN error occurs, THE system SHALL log the event", True),
        ("WHEN user presses hotkey, THE VTT_System SHALL toggle recording", True),
        ("WHEN network connection fails, THE system SHALL use offline mode", True),
        ("WHEN memory usage exceeds threshold, THE system SHALL optimize resources", True),
        ("WHEN user logs out, THE application SHALL clear session data", True),
        ("WHEN file format is unsupported, THE system SHALL show error message", True),
        ("WHEN processing completes, THE system SHALL notify the user", True),
    ])
    def test_event_driven_pattern_validation(self, spec_module, requirement, expected):
        """Test event-driven EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if expected:
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.EVENT_DRIVEN
    
    # State-driven Requirements (WHILE ... THE system SHALL...)
    @pytest.mark.parametrize("requirement,expected", [
        ("WHILE recording is active, THE VTT_System SHALL monitor audio levels", True),
        ("WHILE transcription is running, THE system SHALL display progress", True),
        ("WHILE user is typing, THE application SHALL provide suggestions", True),
        ("WHILE system is idle, THE service SHALL perform maintenance", True),
        ("WHILE connection is established, THE system SHALL sync data", True),
        ("WHILE processing audio, THE VTT_System SHALL show status indicator", True),
        ("WHILE user is authenticated, THE system SHALL allow access", True),
        ("WHILE backup is running, THE system SHALL limit other operations", True),
        ("WHILE in offline mode, THE application SHALL cache operations", True),
        ("WHILE loading data, THE interface SHALL show loading spinner", True),
    ])
    def test_state_driven_pattern_validation(self, spec_module, requirement, expected):
        """Test state-driven EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if expected:
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.STATE_DRIVEN
    
    # Unwanted behavior Requirements (IF ... THEN THE system SHALL...)
    @pytest.mark.parametrize("requirement,expected", [
        ("IF invalid audio format is detected, THEN THE VTT_System SHALL reject the file", True),
        ("IF authentication fails, THEN THE system SHALL deny access", True),
        ("IF memory limit is exceeded, THEN THE application SHALL terminate gracefully", True),
        ("IF network timeout occurs, THEN THE system SHALL retry connection", True),
        ("IF file is corrupted, THEN THE VTT_System SHALL report error", True),
        ("IF user permission is insufficient, THEN THE system SHALL request elevation", True),
        ("IF disk space is low, THEN THE application SHALL warn user", True),
        ("IF configuration is invalid, THEN THE system SHALL use defaults", True),
        ("IF service is unavailable, THEN THE system SHALL queue requests", True),
        ("IF data validation fails, THEN THE system SHALL reject input", True),
    ])
    def test_unwanted_behavior_pattern_validation(self, spec_module, requirement, expected):
        """Test unwanted behavior EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if expected:
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.UNWANTED_BEHAVIOR
    
    # Optional Requirements (WHERE ... THE system SHALL...)
    @pytest.mark.parametrize("requirement,expected", [
        ("WHERE GPU is available, THE VTT_System SHALL use hardware acceleration", True),
        ("WHERE internet connection exists, THE system SHALL sync with cloud", True),
        ("WHERE user has premium account, THE application SHALL enable advanced features", True),
        ("WHERE multiple audio devices are present, THE system SHALL allow selection", True),
        ("WHERE sufficient memory is available, THE VTT_System SHALL use larger models", True),
        ("WHERE user preferences allow, THE system SHALL send notifications", True),
        ("WHERE backup storage exists, THE application SHALL create automatic backups", True),
        ("WHERE admin privileges are granted, THE system SHALL show advanced options", True),
        ("WHERE external service is configured, THE system SHALL integrate functionality", True),
        ("WHERE debugging is enabled, THE application SHALL log detailed information", True),
    ])
    def test_optional_pattern_validation(self, spec_module, requirement, expected):
        """Test optional EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if expected:
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.OPTIONAL
    
    # Invalid/Non-EARS Requirements
    @pytest.mark.parametrize("requirement,expected", [
        ("The system should process audio files", False),
        ("System processes audio", False),
        ("Audio processing functionality", False),
        ("Process audio files", False),
        ("The VTT system will transcribe audio", False),
        ("System must handle errors", False),
        ("Audio transcription capability", False),
        ("Handle user input properly", False),
        ("Good performance is required", False),
        ("User-friendly interface", False),
        ("", False),
        ("   ", False),
        ("THE", False),
        ("SHALL", False),
        ("THE SHALL", False),
        ("THE system", False),
        ("SHALL process", False),
    ])
    def test_invalid_pattern_validation(self, spec_module, requirement, expected):
        """Test validation of invalid/non-EARS requirements."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
        
        if not expected and requirement.strip():
            pattern_type = spec_module._detect_ears_pattern(requirement)
            assert pattern_type == EARSPattern.INVALID
    
    # Case sensitivity tests
    @pytest.mark.parametrize("requirement,expected", [
        ("the vtt_system shall process audio files", True),  # lowercase
        ("The VTT_System Shall Process Audio Files", True),  # mixed case
        ("THE VTT_SYSTEM SHALL PROCESS AUDIO FILES", True),  # uppercase
        ("when user clicks, the system shall respond", True),  # lowercase event
        ("WHEN USER CLICKS, THE SYSTEM SHALL RESPOND", True),  # uppercase event
    ])
    def test_case_insensitive_validation(self, spec_module, requirement, expected):
        """Test case-insensitive EARS pattern validation."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
    
    # Complex requirements with multiple clauses
    @pytest.mark.parametrize("requirement,expected", [
        ("THE VTT_System SHALL process audio files AND generate transcriptions", True),
        ("WHEN user selects file AND clicks process, THE system SHALL start transcription", True),
        ("IF error occurs OR timeout happens, THEN THE system SHALL retry", True),
        ("THE system SHALL validate input BUT allow override with admin privileges", True),
        ("WHILE processing audio OR video, THE system SHALL show progress indicator", True),
    ])
    def test_complex_requirements_validation(self, spec_module, requirement, expected):
        """Test validation of complex requirements with multiple clauses."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
    
    # Requirements with specific formatting variations
    @pytest.mark.parametrize("requirement,expected", [
        ("THE VTT_System SHALL process audio files.", True),  # with period
        ("THE VTT_System SHALL process audio files;", True),  # with semicolon
        ("THE VTT_System SHALL process audio files,", True),  # with comma
        ("THE VTT_System SHALL process audio files!", True),  # with exclamation
        ("THE VTT_System SHALL process audio files?", True),  # with question mark
        ("  THE VTT_System SHALL process audio files  ", True),  # with whitespace
        ("\tTHE VTT_System SHALL process audio files\n", True),  # with tabs/newlines
    ])
    def test_formatting_variations_validation(self, spec_module, requirement, expected):
        """Test validation with various formatting variations."""
        result = spec_module.ensure_ears_compliance(requirement)
        assert result == expected
    
    # Edge cases and boundary conditions
    def test_very_long_requirement(self, spec_module):
        """Test validation of very long requirements."""
        long_requirement = "THE VTT_System SHALL " + "process audio files and " * 100 + "generate transcriptions"
        
        result = spec_module.ensure_ears_compliance(long_requirement)
        assert result is True  # Should still be valid EARS pattern
    
    def test_requirement_with_numbers_and_symbols(self, spec_module):
        """Test validation of requirements with numbers and symbols."""
        requirements = [
            "THE VTT_System SHALL process 44.1kHz audio files",
            "THE system SHALL handle UTF-8 encoded text",
            "THE application SHALL support files up to 2GB in size",
            "THE VTT_System SHALL achieve 95% accuracy",
            "THE system SHALL respond within 100ms ± 10ms"
        ]
        
        for requirement in requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True
    
    def test_requirement_with_technical_terms(self, spec_module):
        """Test validation of requirements with technical terminology."""
        technical_requirements = [
            "THE VTT_System SHALL implement WebRTC for real-time communication",
            "THE system SHALL use HTTPS/TLS for secure data transmission",
            "THE application SHALL support JSON and XML data formats",
            "THE VTT_System SHALL integrate with REST APIs",
            "THE system SHALL implement OAuth 2.0 authentication"
        ]
        
        for requirement in technical_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True
    
    def test_pattern_type_detection_accuracy(self, spec_module):
        """Test accuracy of EARS pattern type detection."""
        test_cases = [
            ("THE system SHALL work", EARSPattern.UBIQUITOUS),
            ("WHEN event occurs, THE system SHALL respond", EARSPattern.EVENT_DRIVEN),
            ("WHILE condition is true, THE system SHALL act", EARSPattern.STATE_DRIVEN),
            ("IF problem occurs, THEN THE system SHALL handle it", EARSPattern.UNWANTED_BEHAVIOR),
            ("WHERE condition exists, THE system SHALL adapt", EARSPattern.OPTIONAL),
            ("The system should work", EARSPattern.INVALID)
        ]
        
        for requirement, expected_pattern in test_cases:
            detected_pattern = spec_module._detect_ears_pattern(requirement)
            assert detected_pattern == expected_pattern
    
    def test_ears_compliance_with_suggestions(self, spec_module):
        """Test EARS compliance checking with suggestion generation."""
        invalid_requirements = [
            "The system should process audio",
            "System must handle errors",
            "Audio processing is required",
            "Handle user input properly"
        ]
        
        for requirement in invalid_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is False
            
            # Test suggestion generation
            suggestions = spec_module._generate_ears_suggestions(requirement, "req_001")
            assert isinstance(suggestions, list)
            assert len(suggestions) > 0
            assert any("SHALL" in suggestion for suggestion in suggestions)
    
    def test_ears_pattern_with_nested_conditions(self, spec_module):
        """Test EARS patterns with nested conditions."""
        nested_requirements = [
            "WHEN user clicks record AND microphone is available, THE VTT_System SHALL start recording",
            "IF (error occurs OR timeout happens) AND retry count < 3, THEN THE system SHALL retry",
            "WHILE (recording is active OR processing is running) AND system resources are available, THE system SHALL continue operation",
            "WHERE (GPU is available AND memory > 4GB) OR high-performance mode is enabled, THE system SHALL use advanced processing"
        ]
        
        for requirement in nested_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True
    
    def test_ears_validation_performance(self, spec_module):
        """Test performance of EARS validation with many requirements."""
        import time
        
        # Generate many requirements for performance testing
        requirements = []
        for i in range(1000):
            requirements.append(f"THE VTT_System SHALL process audio file number {i}")
        
        start_time = time.time()
        
        for requirement in requirements:
            spec_module.ensure_ears_compliance(requirement)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should process 1000 requirements in reasonable time (< 1 second)
        assert processing_time < 1.0
        
        # Average time per requirement should be very small
        avg_time_per_req = processing_time / len(requirements)
        assert avg_time_per_req < 0.001  # Less than 1ms per requirement


class TestEARSPatternEdgeCases:
    """Test edge cases and error conditions for EARS pattern validation."""
    
    @pytest.fixture
    def spec_module(self):
        return SpecComplianceModule()
    
    def test_none_input(self, spec_module):
        """Test EARS validation with None input."""
        result = spec_module.ensure_ears_compliance(None)
        assert result is False
    
    def test_empty_string_input(self, spec_module):
        """Test EARS validation with empty string."""
        result = spec_module.ensure_ears_compliance("")
        assert result is False
    
    def test_whitespace_only_input(self, spec_module):
        """Test EARS validation with whitespace-only input."""
        whitespace_inputs = ["   ", "\t", "\n", "\r\n", " \t \n "]
        
        for input_str in whitespace_inputs:
            result = spec_module.ensure_ears_compliance(input_str)
            assert result is False
    
    def test_special_characters_input(self, spec_module):
        """Test EARS validation with special characters."""
        special_char_requirements = [
            "THE VTT_System SHALL process files with names containing @#$%^&*()",
            "THE system SHALL handle Unicode characters: αβγδε",
            "THE application SHALL support emojis: 🎵🎤🔊",
            "THE VTT_System SHALL process files with paths like C:\\Users\\Test\\Audio.wav"
        ]
        
        for requirement in special_char_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True
    
    def test_malformed_ears_patterns(self, spec_module):
        """Test validation of malformed EARS patterns."""
        malformed_patterns = [
            "THE SHALL process",  # Missing system name
            "VTT_System SHALL process",  # Missing THE
            "THE VTT_System process",  # Missing SHALL
            "WHEN THE system SHALL",  # Incomplete event-driven
            "IF THEN THE system SHALL",  # Missing condition
            "WHILE THE system SHALL",  # Missing state condition
            "WHERE THE system SHALL",  # Missing optional condition
        ]
        
        for pattern in malformed_patterns:
            result = spec_module.ensure_ears_compliance(pattern)
            assert result is False
    
    def test_mixed_language_requirements(self, spec_module):
        """Test EARS validation with mixed language content."""
        # These should be invalid as EARS is English-based
        mixed_language_requirements = [
            "LE système DOIT traiter les fichiers audio",  # French
            "EL sistema DEBE procesar archivos de audio",  # Spanish
            "DAS System SOLL Audiodateien verarbeiten",  # German
            "THE VTT_System SHALL процесс audio files",  # Mixed English/Russian
        ]
        
        for requirement in mixed_language_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            # Only the mixed English one might be valid
            if "THE" in requirement and "SHALL" in requirement:
                assert result is True
            else:
                assert result is False
    
    def test_requirements_with_line_breaks(self, spec_module):
        """Test EARS validation with requirements containing line breaks."""
        multiline_requirements = [
            "THE VTT_System SHALL\nprocess audio files",
            "THE VTT_System\nSHALL process\naudio files",
            "WHEN user clicks record,\nTHE VTT_System SHALL start recording",
            "THE system SHALL process audio files\nand generate transcriptions"
        ]
        
        for requirement in multiline_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True  # Should handle line breaks gracefully
    
    def test_requirements_with_excessive_whitespace(self, spec_module):
        """Test EARS validation with excessive whitespace."""
        whitespace_requirements = [
            "THE    VTT_System    SHALL    process    audio    files",
            "  THE  VTT_System  SHALL  process  audio  files  ",
            "THE\tVTT_System\tSHALL\tprocess\taudio\tfiles",
            "THE VTT_System           SHALL process audio files"
        ]
        
        for requirement in whitespace_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True  # Should normalize whitespace
    
    def test_circular_or_recursive_patterns(self, spec_module):
        """Test EARS validation with potentially problematic patterns."""
        problematic_requirements = [
            "THE system SHALL ensure THE system SHALL work",
            "WHEN THE system SHALL process, THE system SHALL process",
            "THE VTT_System SHALL THE VTT_System SHALL process audio"
        ]
        
        for requirement in problematic_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            # These are technically valid EARS patterns, just poorly written
            assert result is True
    
    def test_extremely_long_system_names(self, spec_module):
        """Test EARS validation with very long system names."""
        long_system_name = "VTT_Advanced_Audio_Processing_And_Transcription_System_With_Machine_Learning_Capabilities"
        requirement = f"THE {long_system_name} SHALL process audio files"
        
        result = spec_module.ensure_ears_compliance(requirement)
        assert result is True
    
    def test_requirements_with_urls_and_paths(self, spec_module):
        """Test EARS validation with URLs and file paths."""
        path_requirements = [
            "THE VTT_System SHALL save files to /usr/local/vtt/output/",
            "THE system SHALL download models from https://example.com/models/",
            "THE application SHALL read config from C:\\Program Files\\VTT\\config.json",
            "THE VTT_System SHALL access API at http://api.example.com/v1/transcribe"
        ]
        
        for requirement in path_requirements:
            result = spec_module.ensure_ears_compliance(requirement)
            assert result is True