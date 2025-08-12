# Atlas Explorer Python API - Optimization & Refactoring TODO

## Executive Summary

This document provides a comprehensive analysis and step-by-step refactoring plan for the `atlasexplorer.py` script. As an expert Python developer, I've identified significant opportunities for optimization, modernization, and architectural improvements while maintaining backwards compatibility and enterprise-grade security.

## 🔍 Current Assessment

### Strengths
- ✅ **Enterprise Security**: Robust hybrid encryption implementation
- ✅ **Comprehensive Functionality**: Complete experiment lifecycle management
- ✅ **Cloud Integration**: Well-designed API communication patterns
- ✅ **ELF Analysis**: Advanced binary inspection capabilities

### Critical Issues Identified
- ❌ **Monolithic Design**: Single 1038-line file violates SRP and makes testing difficult
- ❌ **Poor Error Handling**: Inconsistent exception handling and recovery patterns
- ❌ **Security Vulnerabilities**: Hard-coded cryptographic parameters and unsafe `eval()` usage
- ❌ **No Type Safety**: Missing type hints throughout codebase
- ❌ **Limited Testing**: No visible test infrastructure or validation framework
- ❌ **Mixed Responsibilities**: Classes handle too many concerns
- ❌ **Legacy Patterns**: Outdated Python idioms and anti-patterns

---

## 📋 Refactoring Roadmap

### Phase 1: Foundation & Structure (Priority: CRITICAL)

#### 1.1 Modular Architecture
**Timeline: 3-5 days**

**Current Problem:**
```python
# 1038 lines in single file - violation of Single Responsibility Principle
class Experiment:  # Handles: crypto, networking, ELF parsing, file I/O, reporting
class AtlasExplorer:  # Handles: auth, config, API calls, validation
```

**Proposed Structure:**
```
atlasexplorer/
├── __init__.py                 # Public API exports
├── core/
│   ├── __init__.py
│   ├── client.py              # AtlasExplorer (main client)
│   ├── experiment.py          # Experiment management
│   ├── config.py              # Configuration handling
│   └── constants.py           # Global constants
├── security/
│   ├── __init__.py
│   ├── encryption.py          # Hybrid encryption logic
│   ├── authentication.py     # API key validation
│   └── signed_urls.py         # URL signature handling
├── analysis/
│   ├── __init__.py
│   ├── elf_parser.py          # ELF/DWARF analysis
│   ├── reports.py             # Report generation
│   └── metrics.py             # Performance metrics
├── network/
│   ├── __init__.py
│   ├── api_client.py          # HTTP client wrapper
│   ├── endpoints.py           # API endpoint definitions
│   └── retry.py               # Retry logic with backoff
├── cli/
│   ├── __init__.py
│   ├── commands.py            # CLI command handlers
│   └── interactive.py         # Interactive configuration
└── utils/
    ├── __init__.py
    ├── file_ops.py            # File operations
    ├── validators.py          # Input validation
    └── exceptions.py          # Custom exception classes
```

**Benefits:**
- **Single Responsibility**: Each module has one clear purpose
- **Testability**: Individual components can be unit tested
- **Maintainability**: Changes isolated to specific concerns
- **Reusability**: Components can be reused across different contexts

#### 1.2 Type Safety Implementation
**Timeline: 2-3 days**

**Current Problem:**
```python
def run(self, expname=None, unpack=True):  # No type hints
def addWorkload(self, workload):           # Dynamic typing issues
```

**Proposed Solution:**
```python
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    name: str
    core: str
    workloads: List[Path]
    timeout: int = 300
    unpack: bool = True

class Experiment:
    def run(self, 
           expname: Optional[str] = None, 
           unpack: bool = True) -> ExperimentResult:
        
    def add_workload(self, workload: Union[str, Path]) -> None:
        
    def set_core(self, core: str) -> None:
```

**Benefits:**
- **IDE Support**: Better autocomplete and error detection
- **Runtime Safety**: Early detection of type mismatches
- **Documentation**: Types serve as inline documentation
- **Refactoring Safety**: Easier to refactor with type guarantees

#### 1.3 Custom Exception Hierarchy
**Timeline: 1-2 days**

**Current Problem:**
```python
# Generic exceptions make debugging difficult
except Exception as error:
    print("Encryption error:", error)

# sys.exit() calls throughout - poor error handling
if not os.path.exists(workload):
    print(f"Error: specified elf file does not exist\nELF: {workload}")
    sys.exit(1)
```

**Proposed Solution:**
```python
# utils/exceptions.py
class AtlasExplorerError(Exception):
    """Base exception for all Atlas Explorer errors."""
    pass

class AuthenticationError(AtlasExplorerError):
    """Raised when API authentication fails."""
    pass

class NetworkError(AtlasExplorerError):
    """Raised for network-related failures."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class EncryptionError(AtlasExplorerError):
    """Raised when encryption/decryption operations fail."""
    pass

class ELFValidationError(AtlasExplorerError):
    """Raised when ELF file validation fails."""
    def __init__(self, message: str, file_path: Path):
        super().__init__(message)
        self.file_path = file_path

class ExperimentError(AtlasExplorerError):
    """Raised during experiment execution."""
    def __init__(self, message: str, experiment_id: Optional[str] = None):
        super().__init__(message)
        self.experiment_id = experiment_id

# Usage example:
def add_workload(self, workload: Union[str, Path]) -> None:
    workload_path = Path(workload)
    if not workload_path.exists():
        raise ELFValidationError(
            f"ELF file not found: {workload_path}", 
            workload_path
        )
```

**Benefits:**
- **Precise Error Handling**: Catch specific exception types
- **Better Debugging**: Rich context in exception objects
- **Graceful Degradation**: No more sys.exit() calls
- **API Consistency**: Predictable error patterns for users

---

### Phase 2: Security Hardening (Priority: HIGH)

#### 2.1 Cryptographic Security Improvements
**Timeline: 3-4 days**

**Current Vulnerabilities:**
```python
# CRITICAL: Hard-coded salt in scrypt - major security flaw
key = scrypt(password.encode(), salt=b"salt", key_len=32, N=16384, r=8, p=1)

# Unsafe eval() usage - code injection vulnerability
eval(args.handler_function + "(args)")

# Mixed crypto libraries (pycryptodome + cryptography)
from Crypto.Cipher import AES  # Legacy library
from cryptography.hazmat.primitives.ciphers import Cipher  # Modern library
```

**Proposed Security Hardening:**
```python
# security/encryption.py
import secrets
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureEncryption:
    """Enterprise-grade encryption with security best practices."""
    
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key using scrypt with secure parameters."""
        kdf = Scrypt(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            n=2**17,  # Increased work factor
            r=8,
            p=1,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))
    
    @staticmethod
    def generate_salt() -> bytes:
        """Generate cryptographically secure random salt."""
        return secrets.token_bytes(32)
    
    def encrypt_file(self, file_path: Path, public_key_pem: str) -> bytes:
        """Implement secure hybrid encryption with random salts."""
        # Use AESGCM for authenticated encryption
        # Generate unique salt per encryption
        # Implement proper key derivation
```

**Security Improvements:**
- **Random Salts**: No more hard-coded cryptographic values
- **Increased Work Factors**: Better resistance to brute force
- **Unified Crypto Library**: Use only `cryptography` (modern, audited)
- **Remove eval()**: Replace with secure dispatch mechanism

#### 2.2 Input Validation Framework
**Timeline: 2-3 days**

**Current Problem:**
```python
# No input validation
def setCore(self, core):
    self.core = core  # Could be None, empty, or malicious

# Unsafe file operations
with open(content, "rb") if isinstance(content, str) else content as data:
```

**Proposed Solution:**
```python
# utils/validators.py
from pathlib import Path
import re
from typing import Set

class Validators:
    """Comprehensive input validation framework."""
    
    VALID_CORES: Set[str] = {'I8500', 'P8500', 'A8700', 'M8700'}
    CORE_PATTERN = re.compile(r'^[A-Z]\d{4}$')
    
    @staticmethod
    def validate_core(core: str) -> str:
        """Validate processor core identifier."""
        if not isinstance(core, str):
            raise ValueError("Core must be a string")
        
        core = core.strip().upper()
        if not core:
            raise ValueError("Core cannot be empty")
            
        if not Validators.CORE_PATTERN.match(core):
            raise ValueError(f"Invalid core format: {core}")
            
        if core not in Validators.VALID_CORES:
            raise ValueError(f"Unsupported core: {core}")
            
        return core
    
    @staticmethod
    def validate_elf_file(file_path: Union[str, Path]) -> Path:
        """Comprehensive ELF file validation."""
        path = Path(file_path)
        
        if not path.exists():
            raise ELFValidationError(f"File not found: {path}", path)
            
        if not path.is_file():
            raise ELFValidationError(f"Not a regular file: {path}", path)
            
        # Check file size (prevent DoS)
        if path.stat().st_size > 100 * 1024 * 1024:  # 100MB limit
            raise ELFValidationError(f"File too large: {path}", path)
            
        # Validate ELF magic number
        with path.open('rb') as f:
            magic = f.read(4)
            if magic != b'\x7fELF':
                raise ELFValidationError(f"Not an ELF file: {path}", path)
                
        return path
```

#### 2.3 Secure Configuration Management
**Timeline: 2 days**

**Current Problem:**
```python
# Plain text credential storage
config = {
    "apikey": apikey,  # Stored in plain text
    "channel": chanswer,
    "region": regionanswer,
}
```

**Proposed Solution:**
```python
# security/credential_manager.py
import keyring
from cryptography.fernet import Fernet

class SecureCredentialManager:
    """Secure credential storage using OS keyring."""
    
    def __init__(self):
        self.service_name = "mips-atlas-explorer"
        
    def store_credentials(self, username: str, credentials: Dict[str, str]) -> None:
        """Store encrypted credentials in OS keyring."""
        # Encrypt sensitive data before keyring storage
        encrypted_data = self._encrypt_dict(credentials)
        keyring.set_password(self.service_name, username, encrypted_data)
    
    def get_credentials(self, username: str) -> Dict[str, str]:
        """Retrieve and decrypt credentials from OS keyring."""
        encrypted_data = keyring.get_password(self.service_name, username)
        if not encrypted_data:
            raise AuthenticationError("No stored credentials found")
        return self._decrypt_dict(encrypted_data)
```

---

### Phase 3: Network & API Improvements (Priority: MEDIUM)

#### 3.1 Robust HTTP Client
**Timeline: 2-3 days**

**Current Problem:**
```python
# No retry logic, timeouts, or connection pooling
resp = requests.post(url, headers=myobj)  # Can hang indefinitely
x = requests.get(url, headers=myobj)      # No error handling
```

**Proposed Solution:**
```python
# network/api_client.py
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class AtlasAPIClient:
    """Enterprise HTTP client with retry logic and proper error handling."""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = httpx.Timeout(timeout)
        self.headers = {"apikey": api_key}
        
        # Connection pooling for better performance
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=5)
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request with automatic retry and error handling."""
        try:
            response = await self.client.post(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.TimeoutException:
            raise NetworkError(f"Request timeout for {endpoint}")
        except httpx.HTTPStatusError as e:
            raise NetworkError(f"HTTP {e.response.status_code}: {e.response.text}")
```

#### 3.2 Asynchronous Operations
**Timeline: 3-4 days**

**Current Problem:**
```python
# Blocking operations throughout
while count < 10:
    count += 1
    time.sleep(2)  # Blocking sleep
    status = self.__getStatus(statusURL)  # Blocking HTTP
```

**Proposed Solution:**
```python
# core/experiment.py
import asyncio
from typing import AsyncGenerator

class AsyncExperiment:
    """Asynchronous experiment execution with real-time progress."""
    
    async def run(self, config: ExperimentConfig) -> AsyncGenerator[ExperimentStatus, None]:
        """Run experiment with async status updates."""
        # Upload phase
        yield ExperimentStatus.UPLOADING
        upload_result = await self._upload_package(config)
        
        # Processing phase with real-time updates
        yield ExperimentStatus.PROCESSING
        async for status in self._monitor_progress(upload_result.status_url):
            yield status
            
        # Download phase
        yield ExperimentStatus.DOWNLOADING
        results = await self._download_results(upload_result.download_url)
        
        yield ExperimentStatus.COMPLETE(results)
    
    async def _monitor_progress(self, status_url: str) -> AsyncGenerator[ExperimentStatus, None]:
        """Monitor experiment progress with exponential backoff."""
        backoff = 1
        max_backoff = 30
        
        while True:
            try:
                status = await self.api_client.get_status(status_url)
                yield ExperimentStatus.from_api_response(status)
                
                if status.is_terminal():
                    break
                    
                await asyncio.sleep(min(backoff, max_backoff))
                backoff *= 1.5
                
            except NetworkError as e:
                yield ExperimentStatus.ERROR(str(e))
                break
```

---

### Phase 4: Testing & Quality Assurance (Priority: HIGH)

#### 4.1 Comprehensive Test Suite
**Timeline: 4-5 days**

**Current Problem:**
- No visible test infrastructure
- No validation of critical security functions
- No integration tests for API interactions

**Proposed Solution:**
```
tests/
├── unit/
│   ├── test_encryption.py      # Crypto functions
│   ├── test_validators.py      # Input validation
│   ├── test_config.py          # Configuration handling
│   └── test_elf_parser.py      # ELF analysis
├── integration/
│   ├── test_api_client.py      # API interactions
│   ├── test_experiment_flow.py # End-to-end workflows
│   └── test_auth.py            # Authentication flows
├── fixtures/
│   ├── sample.elf              # Test ELF files
│   ├── mock_responses.json     # API response mocks
│   └── test_configs.py         # Test configurations
└── conftest.py                 # Pytest configuration
```

**Example Test Implementation:**
```python
# tests/unit/test_encryption.py
import pytest
from pathlib import Path
from atlasexplorer.security.encryption import SecureEncryption
from atlasexplorer.utils.exceptions import EncryptionError

class TestSecureEncryption:
    """Comprehensive encryption security tests."""
    
    def test_salt_uniqueness(self):
        """Ensure salt generation produces unique values."""
        salts = [SecureEncryption.generate_salt() for _ in range(100)]
        assert len(set(salts)) == 100, "Salt generation must be unique"
    
    def test_key_derivation_consistency(self):
        """Verify key derivation is deterministic with same inputs."""
        password = "test_password"
        salt = b"fixed_salt_for_testing"
        
        key1 = SecureEncryption.derive_key(password, salt)
        key2 = SecureEncryption.derive_key(password, salt)
        
        assert key1 == key2, "Key derivation must be deterministic"
    
    def test_encryption_roundtrip(self, tmp_path):
        """Test encryption/decryption roundtrip integrity."""
        test_file = tmp_path / "test.bin"
        test_data = b"sensitive_experiment_data" * 1000
        test_file.write_bytes(test_data)
        
        # Generate test keypair
        private_key, public_key_pem = self._generate_test_keypair()
        
        # Encrypt
        encryption = SecureEncryption()
        encrypted_data = encryption.encrypt_file(test_file, public_key_pem)
        
        # Decrypt
        decrypted_data = encryption.decrypt_file(encrypted_data, private_key)
        
        assert decrypted_data == test_data, "Encryption roundtrip failed"
    
    def test_tamper_detection(self):
        """Verify tampered ciphertext is detected."""
        # Test that modified ciphertext raises EncryptionError
        pass
```

#### 4.2 Security Testing
**Timeline: 2-3 days**

```python
# tests/security/test_crypto_security.py
class TestCryptographicSecurity:
    """Security-focused cryptographic testing."""
    
    def test_no_hardcoded_secrets(self):
        """Scan codebase for hardcoded cryptographic materials."""
        # Regex patterns for common hardcoded secrets
        patterns = [
            r'salt=b["\'][^"\']+["\']',  # Hardcoded salts
            r'key=["\'][a-zA-Z0-9+/=]{20,}["\']',  # Base64 keys
            r'password=["\'][^"\']+["\']',  # Hardcoded passwords
        ]
        
        # Scan source files
        violations = self._scan_source_files(patterns)
        assert not violations, f"Hardcoded secrets found: {violations}"
    
    def test_timing_attack_resistance(self):
        """Test key derivation timing attack resistance."""
        import time
        
        password = "test_password"
        salt = SecureEncryption.generate_salt()
        
        # Measure timing for multiple iterations
        times = []
        for _ in range(10):
            start = time.perf_counter()
            SecureEncryption.derive_key(password, salt)
            times.append(time.perf_counter() - start)
        
        # Verify timing is consistent (not data-dependent)
        avg_time = sum(times) / len(times)
        for t in times:
            assert abs(t - avg_time) / avg_time < 0.1, "Timing variation too high"
```

#### 4.3 Performance & Load Testing
**Timeline: 2 days**

```python
# tests/performance/test_load.py
import asyncio
import pytest
from atlasexplorer.core.experiment import AsyncExperiment

class TestPerformance:
    """Performance and scalability testing."""
    
    @pytest.mark.asyncio
    async def test_concurrent_experiments(self):
        """Test handling of multiple concurrent experiments."""
        experiments = [AsyncExperiment() for _ in range(10)]
        
        # Run experiments concurrently
        start_time = asyncio.get_event_loop().time()
        results = await asyncio.gather(*[
            exp.run(test_config) for exp in experiments
        ])
        end_time = asyncio.get_event_loop().time()
        
        # Verify all completed successfully
        assert all(r.success for r in results)
        
        # Performance assertion
        assert end_time - start_time < 60, "Concurrent experiments too slow"
    
    def test_memory_usage(self):
        """Monitor memory usage during large operations."""
        import tracemalloc
        
        tracemalloc.start()
        
        # Perform memory-intensive operations
        experiment = Experiment("test_dir", mock_atlas)
        experiment.add_workload(large_elf_file)
        experiment.run()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Assert reasonable memory usage (adjust threshold as needed)
        assert peak < 500 * 1024 * 1024, f"Memory usage too high: {peak} bytes"
```

---

### Phase 5: Developer Experience & Tooling (Priority: MEDIUM)

#### 5.1 Development Environment
**Timeline: 1-2 days**

**Create Modern Development Infrastructure:**
```yaml
# .github/workflows/ci.yml
name: Continuous Integration
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e .[dev,test]
        
    - name: Lint with ruff
      run: ruff check atlasexplorer/
      
    - name: Type check with mypy
      run: mypy atlasexplorer/
      
    - name: Security scan with bandit
      run: bandit -r atlasexplorer/
      
    - name: Test with pytest
      run: pytest tests/ --cov=atlasexplorer --cov-report=xml
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mips-atlas-explorer"
version = "1.0.0"
description = "MIPS Atlas Explorer Python API"
dependencies = [
    "httpx>=0.24.0",
    "cryptography>=41.0.0",
    "pyelftools>=0.29",
    "tenacity>=8.2.0",
    "pydantic>=2.0.0",
    "keyring>=24.0.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.0.290",
    "mypy>=1.5.0",
    "black>=23.0.0",
    "pre-commit>=3.0.0",
]
test = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "bandit>=1.7.5",
]

[tool.ruff]
select = ["E", "F", "I", "N", "W", "UP", "S", "B", "A", "C4", "T20"]
ignore = ["E501"]  # Line length handled by black

[tool.mypy]
python_version = "3.8"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "--strict-markers --disable-warnings"
```

#### 5.2 Enhanced CLI Interface
**Timeline: 2-3 days**

**Current Problem:**
```python
# Limited CLI with only configure command
if __name__ == "__main__":
    parser = argparse.ArgumentParser(...)
    # Only supports 'configure'
```

**Proposed Rich CLI:**
```python
# cli/commands.py
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

app = typer.Typer(name="atlas-explorer", help="MIPS Atlas Explorer CLI")
console = Console()

@app.command()
def configure(
    interactive: bool = typer.Option(True, help="Interactive configuration"),
    api_key: Optional[str] = typer.Option(None, help="API key"),
    channel: Optional[str] = typer.Option(None, help="Channel"),
    region: Optional[str] = typer.Option(None, help="Region"),
):
    """Configure Atlas Explorer credentials and settings."""
    if interactive:
        configure_interactive()
    else:
        configure_direct(api_key, channel, region)

@app.command()
def run(
    elf_files: List[Path] = typer.Argument(..., help="ELF files to analyze"),
    core: str = typer.Option("I8500", help="Target processor core"),
    output_dir: Path = typer.Option("experiments", help="Output directory"),
    name: Optional[str] = typer.Option(None, help="Experiment name"),
):
    """Run performance analysis experiment."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing experiment...", total=None)
        
        # Create and run experiment with progress updates
        experiment = create_experiment(output_dir, elf_files, core)
        
        progress.update(task, description="Uploading workloads...")
        # ... upload logic
        
        progress.update(task, description="Processing on cloud...")
        # ... processing logic
        
        progress.update(task, description="Downloading results...")
        # ... download logic

@app.command()
def status(experiment_id: str):
    """Check status of running experiment."""
    status = get_experiment_status(experiment_id)
    
    table = Table(title=f"Experiment {experiment_id} Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Status", status.state.value)
    table.add_row("Progress", f"{status.progress}%")
    table.add_row("Elapsed Time", str(status.elapsed_time))
    
    console.print(table)

@app.command()
def list_experiments(
    limit: int = typer.Option(10, help="Number of experiments to show")
):
    """List recent experiments."""
    # Implementation for listing experiments
```

#### 5.3 Documentation & Examples
**Timeline: 2 days**

**Enhanced Documentation Structure:**
```
docs/
├── getting-started.md          # Quick start guide
├── api-reference/              # Auto-generated API docs
├── examples/                   # Code examples
│   ├── basic_usage.py
│   ├── advanced_analysis.py
│   ├── batch_processing.py
│   └── async_workflows.py
├── security/                   # Security documentation
│   ├── encryption.md
│   ├── authentication.md
│   └── best_practices.md
└── development/                # Developer docs
    ├── contributing.md
    ├── architecture.md
    └── testing.md
```

---

### Phase 6: Performance & Monitoring (Priority: LOW)

#### 6.1 Telemetry & Monitoring
**Timeline: 2-3 days**

```python
# monitoring/telemetry.py
import structlog
from prometheus_client import Counter, Histogram, Gauge
from typing import Optional

# Metrics collection
EXPERIMENTS_TOTAL = Counter('atlas_experiments_total', 'Total experiments run')
EXPERIMENT_DURATION = Histogram('atlas_experiment_duration_seconds', 'Experiment execution time')
ACTIVE_EXPERIMENTS = Gauge('atlas_active_experiments', 'Currently running experiments')

logger = structlog.get_logger()

class TelemetryCollector:
    """Collect performance and usage metrics."""
    
    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        self.logger = logger.bind(experiment_id=experiment_id)
    
    def record_experiment_start(self):
        """Record experiment start metrics."""
        EXPERIMENTS_TOTAL.inc()
        ACTIVE_EXPERIMENTS.inc()
        self.logger.info("experiment_started")
    
    def record_experiment_complete(self, duration: float, success: bool):
        """Record experiment completion metrics."""
        EXPERIMENT_DURATION.observe(duration)
        ACTIVE_EXPERIMENTS.dec()
        
        self.logger.info(
            "experiment_completed",
            duration=duration,
            success=success
        )
```

#### 6.2 Caching & Performance
**Timeline: 2 days**

```python
# utils/cache.py
import asyncio
from functools import wraps
from typing import Dict, Any, Optional
import hashlib
import json

class ExperimentCache:
    """Intelligent caching for experiment results."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, elf_path: Path, core: str) -> str:
        """Generate deterministic cache key."""
        # Include ELF file hash and core in key
        with elf_path.open('rb') as f:
            elf_hash = hashlib.sha256(f.read()).hexdigest()
        
        key_data = {
            'elf_hash': elf_hash,
            'core': core,
            'version': API_EXT_VERSION
        }
        
        return hashlib.sha256(
            json.dumps(key_data, sort_keys=True).encode()
        ).hexdigest()
    
    async def get_cached_result(self, cache_key: str) -> Optional[ExperimentResult]:
        """Retrieve cached experiment result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            # Verify cache freshness (e.g., 24 hours)
            if (time.time() - cache_file.stat().st_mtime) < 86400:
                return ExperimentResult.from_json(cache_file.read_text())
        return None
```

---

## 🛡️ Security Review Checklist

### Critical Security Issues to Address

1. **❌ CRITICAL: Hard-coded Salt**
   - **Location**: Line 156 - `salt=b"salt"`
   - **Risk**: Breaks password-based encryption completely
   - **Fix**: Generate unique salts per encryption

2. **❌ CRITICAL: Code Injection**
   - **Location**: Line 1037 - `eval(args.handler_function + "(args)")`
   - **Risk**: Arbitrary code execution vulnerability
   - **Fix**: Use secure dispatch pattern

3. **❌ HIGH: Mixed Crypto Libraries**
   - **Risk**: Different security models and potential conflicts
   - **Fix**: Standardize on `cryptography` library only

4. **❌ MEDIUM: No Input Validation**
   - **Risk**: Various injection and DoS attacks
   - **Fix**: Comprehensive input validation framework

5. **❌ MEDIUM: Plain Text Credential Storage**
   - **Risk**: Credential exposure
   - **Fix**: OS keyring integration with encryption

---

## 📊 Implementation Priority Matrix

| Priority | Phase | Effort | Impact | Risk |
|----------|-------|--------|--------|------|
| CRITICAL | Security Hardening | High | High | High |
| HIGH | Foundation & Structure | High | High | Medium |
| HIGH | Testing & QA | Medium | High | Low |
| MEDIUM | Network & API | Medium | Medium | Low |
| MEDIUM | Developer Experience | Low | Medium | Low |
| LOW | Performance & Monitoring | Low | Low | Low |

---

## 🔄 Migration Strategy

### Backwards Compatibility Plan

1. **Maintain Current API**: Keep existing public interface intact
2. **Gradual Deprecation**: Warn about deprecated patterns
3. **Adapter Pattern**: Bridge old and new implementations
4. **Comprehensive Testing**: Ensure no regression in functionality

### Example Migration:
```python
# Legacy compatibility layer
from atlasexplorer.legacy import Experiment as LegacyExperiment
from atlasexplorer.core.experiment import Experiment
import warnings

class ExperimentAdapter(Experiment):
    """Backwards compatibility adapter."""
    
    def run(self, expname=None, unpack=True):
        warnings.warn(
            "Legacy run() method is deprecated. Use async run_async() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Adapt to new async interface
        import asyncio
        return asyncio.run(self.run_async(expname, unpack))
```

---

## 🎯 Success Metrics

### Code Quality Metrics
- **Test Coverage**: > 90%
- **Type Coverage**: > 95%  
- **Security Scan**: 0 high/critical issues
- **Performance**: < 2s CLI startup time

### Developer Experience
- **Documentation**: Complete API reference
- **Examples**: 10+ working examples
- **CI/CD**: Full automation pipeline
- **IDE Support**: Full IntelliSense/autocomplete

### Security Posture
- **Zero Hardcoded Secrets**: Automated scanning
- **Secure Defaults**: All operations secure by default
- **Vulnerability Management**: Regular security audits
- **Compliance**: Follow industry security standards

---

## 📝 Next Steps

1. **Team Review**: Present this plan to development team
2. **Security Audit**: External security review of current code
3. **Prototype**: Build proof-of-concept for new architecture
4. **Migration Plan**: Detailed implementation timeline
5. **Resource Allocation**: Assign developers to specific phases

This refactoring plan transforms the Atlas Explorer from a functional but monolithic script into a modern, secure, maintainable Python application that follows industry best practices while maintaining full backwards compatibility.
