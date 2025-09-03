# MIPS ATLAS Explorer Python Library

<div align="center">
  <img src="assets/mips-logo.png" alt="MIPS Logo" width="300" style="margin: 20px;">
</div>

## 🚀 Advanced CPU Performance Analysis Made Easy

**ATLAS Explorer** is MIPS' cutting-edge cloud-based performance analysis platform that enables deep insights into CPU behavior, parallel computing efficiency, and optimization opportunities. This Python library provides seamless access to ATLAS Explorer's powerful simulation capabilities through intuitive **Jupyter notebooks** and flexible **command-line tools**.

### ✨ What Makes ATLAS Explorer Special

🎯 **Real Hardware Simulation** - Accurate models of MIPS I8500 and other advanced CPU architectures  
🔬 **Deep Performance Insights** - Cycle-accurate analysis with comprehensive metrics  
🚀 **Multicore Analysis** - Parallel computing performance and scaling studies  
💡 **Beginner-Friendly** - Interactive Jupyter notebooks with step-by-step guidance  
⚡ **Production Ready** - Command-line tools for automated performance testing  
## 🎓 Getting Started - Choose Your Path

### 📊 **Interactive Analysis (Recommended for Beginners)**

Our **enhanced Jupyter notebooks** provide a guided, educational experience perfect for learning CPU performance analysis:

#### **Single-Core Performance Analysis**
```bash
# Launch the comprehensive single-core analysis notebook
uv run jupyter notebook notebooks/ae_singlecore_notebook.ipynb
```

**What you'll learn:**
- 🧮 CPU instruction execution efficiency (IPC analysis)
- 💾 Cache performance and memory hierarchy behavior  
- 🎯 Bottleneck identification and optimization strategies
- 📈 Performance metrics interpretation and insights
- 🔍 Interactive exploration of detailed results

#### **Multicore & Parallel Computing Analysis**
```bash
# Explore advanced parallel performance analysis
uv run jupyter notebook notebooks/ae_multicore_notebook.ipynb
```

**What you'll master:**
- 🖥️ Thread load balancing and parallel efficiency
- ⚡ Resource contention analysis and optimization
- 📊 Scaling studies across different core counts  
- 🔄 Cache sharing and memory system behavior
- 🚀 Advanced multicore optimization techniques

### ⚡ **Command-Line Tools (For Automation & CI/CD)**

Perfect for scripted performance testing and continuous integration:

```bash
# Single core experiment
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf

# Multicore experiment  
uv run examples/ae_multicore.py --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf
```

## 🛠️ Installation & Setup

### 📋 Prerequisites

- **Python 3.12** (required for optimal compatibility)
- **[uv](https://github.com/astral-sh/uv)** (recommended for dependency management)
- **Git** (for cloning the repository)
- **Jupyter** (for interactive notebook experience)

### 🚀 Quick Setup (3 Steps)

1. **Clone and enter the repository:**
   ```bash
   git clone https://github.com/MIPS/mips-ae-pylib.git
   cd mips-ae-pylib
   ```

2. **Set up environment and install dependencies:**
   ```bash
   uv sync --group notebooks             # Install all dependencies including Jupyter notebook support
   uv pip install -e .                   # Install the atlasexplorer package in development mode
   ```
   > 💡 **Note**: This project uses modern `uv` dependency management. The `uv sync` command automatically creates a virtual environment and installs all dependencies. The `uv pip install -e .` command installs the `atlasexplorer` package so it can be imported from anywhere in the project.

3. **Configure your ATLAS Explorer credentials:**
   ```bash
   uv run atlasexplorer/atlasexplorer.py configure
   ```
   This will prompt for your API key, channel, and region, then save them securely.

### 🎯 Launch Your First Analysis

**For interactive learning (recommended):**
```bash
uv run jupyter notebook notebooks/ae_singlecore_notebook.ipynb
```

**For quick command-line testing:**
```bash
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development
```

> 💡 **New to ATLAS Explorer?** Start with the single-core notebook - it includes comprehensive tutorials and real-world examples!

## 🔐 Configuration Guide

ATLAS Explorer requires cloud credentials for accessing simulation services. We provide multiple convenient configuration methods:

### 🎯 Interactive Setup (Recommended)

```bash
uv run atlasexplorer/atlasexplorer.py configure
```

This guided setup will:
- ✅ Prompt for your API key, channel, and region
- ✅ Validate your credentials with ATLAS Explorer cloud
- ✅ Save credentials securely in both user config and project `.env` file
- ✅ Set up automatic authentication for notebooks and CLI tools

### 🌐 Environment Variables (For CI/CD)

```bash
export MIPS_ATLAS_CONFIG=<apikey>:<channel>:<region>
```

**For GitHub Actions:**
```yaml
env:
  MIPS_ATLAS_CONFIG: ${{ secrets.MIPS_ATLAS_CONFIG }}
```

### 📁 Configuration File Locations

- **User Config**: `~/.config/mips/atlaspy/config.json` (persistent across projects)
- **Project Config**: `.env` file in project root (auto-generated after setup)

### ⚙️ API Version Management

Override the API version for testing or compatibility:
```bash
export API_EXT_VERSION=0.0.97  # Optional: specify API version
```

## 📚 Usage Guide

### 🎓 **Interactive Learning with Jupyter Notebooks (Recommended)**

Our enhanced notebooks provide comprehensive, beginner-friendly guidance for CPU performance analysis:

#### 🧮 Single-Core Analysis Notebook

```bash
# Launch Jupyter and open the single-core analysis notebook
uv run jupyter notebook notebooks/ae_singlecore_notebook.ipynb
```

**Perfect for learning:**
- 📈 **Performance Fundamentals** - IPC, cache behavior, execution efficiency
- 🔍 **Real Experiment Analysis** - Step-by-step analysis of Mandelbrot fractal computation
- 💡 **Optimization Insights** - Identifying bottlenecks and improvement opportunities  
- 📊 **Interactive Exploration** - Filter and analyze 50+ performance metrics
- 🎯 **Beginner-Friendly** - Clear explanations, visual cues, and expert guidance

**Key Results You'll See:**
- ⚡ 253,629 cycles execution time
- 🧮 196,626 instructions with 0.775 IPC efficiency  
- 💾 99.96% cache hit rates (excellent memory performance)
- 🎲 Exceptional branch prediction accuracy

#### 🚀 Multicore Analysis Notebook  

```bash
# Launch the advanced parallel computing analysis
uv run jupyter notebook notebooks/ae_multicore_notebook.ipynb
```

**Master parallel computing:**
- 🖥️ **Thread Load Balancing** - Perfect distribution analysis (196,626 instructions per thread!)
- ⚡ **Parallel Efficiency** - 92% scaling efficiency with 1.429 combined IPC
- 💾 **Resource Sharing** - Cache performance under parallel load (maintained 99%+ hit rates)
- 🔧 **Execution Unit Analysis** - ALU/FPU load distribution and optimization
- 📊 **Scaling Studies** - Framework for 4, 8, 16+ core experiments

**Outstanding Real Results:**  
- 🏆 Perfect load balance (identical instruction counts per thread)
- ✨ Exceptional parallel efficiency (only 8.5% overhead)
- 💾 Maintained cache excellence under parallel load
- 🎯 Ready for aggressive scaling to higher core counts

### ⚙️ **Command-Line Tools for Automation**

Perfect for CI/CD, scripting, and batch processing:

#### Single-Core Experiments
```bash
# Basic single-core analysis
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --channel development --core "I8500_(1_thread)"

# With custom settings
uv run examples/ae_singlecore.py \
  --elf resources/mandelbrot_rv64_O3.elf \
  --channel production \
  --core "I8500_(1_thread)" \
  --expdir my_experiments \
  --verbose
```

#### Multicore Experiments
```bash
# Multi-workload parallel analysis  
uv run examples/ae_multicore.py \
  --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf \
  --channel development \
  --core "I8500_(2_threads)"

# Advanced multicore configurations
uv run examples/ae_multicore.py \
  --elf resources/mandelbrot_rv64_O0.elf resources/memcpy_rv64.elf \
  --core "I8500_(4_threads)" \
  --expdir multicore_scaling_study \
  --region us-west-2
```

### 🔬 **What You Can Analyze**

**Supported Workloads:**
- 🧮 `mandelbrot_rv64_O0.elf` - Compute-intensive floating-point workload
- 🚀 `mandelbrot_rv64_O3.elf` - Optimized version for compiler comparison
- 💾 `memcpy_rv64.elf` - Memory-intensive data movement workload

**CPU Architectures:**
- 🖥️ I8500_(1_thread) - Single-core configuration  
- ⚡ I8500_(2_threads) - Dual-core parallel processing
- 🚀 I8500_(4_threads) - Quad-core scaling studies
- 🔥 Custom configurations available

**Performance Metrics:**
- ⚡ Execution cycles and IPC efficiency
- 💾 L1/L2 cache hit rates and memory performance
- 🎲 Branch prediction accuracy and pipeline efficiency  
- 🔧 Execution unit utilization (ALU, FPU, LSU)
- 🧵 Thread balancing and parallel scaling
- 📊 50+ detailed microarchitectural metrics

## 🧪 Testing & Development

### 🚀 Quick Testing

```bash
# Run all tests 
uv run python -m pytest -s

# Run all tests with coverage (if pytest-cov is installed)
uv run python -m pytest -s --cov=atlasexplorer

# Test specific functionality
uv run python -m pytest -s tests/test_ae_singlecore.py
uv run python -m pytest -s tests/test_ae_multicore.py
```

### 🔧 Development Setup

```bash
# Install all dependencies including development tools
uv sync --group dev

# Install the package in development mode
uv pip install -e .

# Run tests with coverage
uv run python -m pytest -s --cov=atlasexplorer

# Test specific functionality
uv run python -m pytest -s tests/test_ae_singlecore.py
uv run python -m pytest -s tests/test_ae_multicore.py
```

### 📊 CI/CD Integration

The project includes GitHub Actions workflows that:
- ✅ Test across multiple Python versions
- ✅ Run comprehensive performance analysis tests
- ✅ Validate notebook functionality  
- ✅ Use `MIPS_ATLAS_CONFIG` secret for cloud authentication

## 🌟 Example Results

### Single-Core Performance Analysis

```
🎯 KEY RESULT: Total Cycles: 253,627
📊 Instructions Executed: 196,626  
⚡ IPC (Instructions Per Cycle): 0.775
💾 L1 Instruction Cache Hit Rate: 99.96%
💾 L1 Data Cache Hit Rate: 99.86%  
🎲 Branch Mispredictions: 0.73 per 1K instructions
```

### Multicore Performance Analysis  

```
🚀 Multicore Total Cycles: 257,648
⚖️ Perfect Load Balance: 196,626 instructions per thread
⚡ Combined IPC: 1.429 (92% scaling efficiency)
🏆 Thread 0 IPC: 0.714 | Thread 1 IPC: 0.715
💾 Cache Hit Rates Maintained: >99% under parallel load
```

## 📁 Project Structure

```
mips-ae-pylib/
├── 📓 notebooks/                    # 🌟 Enhanced Jupyter Notebooks
│   ├── ae_singlecore_notebook.ipynb    # Single-core analysis with tutorials
│   └── ae_multicore_notebook.ipynb     # Multicore & parallel computing
├── 📦 atlasexplorer/                # Core library
│   ├── __init__.py
│   └── atlasexplorer.py
├── 🎯 examples/                     # Command-line tools  
│   ├── ae_singlecore.py                # Single-core experiments
│   └── ae_multicore.py                 # Multicore experiments
├── 📊 resources/                    # Sample workloads
│   ├── mandelbrot_rv64_O0.elf          # Compute-intensive (unoptimized)
│   ├── mandelbrot_rv64_O3.elf          # Compute-intensive (optimized)
│   └── memcpy_rv64.elf                 # Memory-intensive
├── 🧪 tests/                       # Test suite
│   ├── test_ae_singlecore.py
│   └── test_ae_multicore.py  
├── 🎨 assets/                      # Images and branding
│   └── mips-logo.png
├── 📁 myexperiments/               # Experiment results (auto-generated)
├── ⚙️ Configuration files
│   ├── .env                            # Local credentials (auto-generated)
│   ├── env-example                     # Template for manual setup
│   ├── pyproject.toml                  # Project metadata
│   └── setup.py                        # Python packaging
└── 📖 README.md                    # This guide
```

## 🎯 Learning Paths

### 🌱 **For Performance Analysis Beginners**

1. **Start Here**: `notebooks/ae_singlecore_notebook.ipynb`
   - Learn CPU performance fundamentals
   - Understand IPC, cache behavior, and optimization
   - Explore real experimental data with guided explanations

2. **Next Level**: `notebooks/ae_multicore_notebook.ipynb`  
   - Master parallel computing concepts
   - Analyze thread load balancing and scaling
   - Understand resource contention and optimization

3. **Advanced Practice**: Command-line experiments
   - Automate performance testing workflows
   - Compare different optimizations (-O0 vs -O3)
   - Build custom analysis pipelines

### 🚀 **For Performance Engineers**

1. **Quick Start**: Command-line tools for immediate analysis
2. **Deep Dive**: Jupyter notebooks for comprehensive insights
3. **Scale Up**: Multi-configuration experiments and comparative studies
4. **Integrate**: CI/CD pipeline integration for continuous performance monitoring

### 👨‍💻 **For Developers & Researchers**

1. **Library Integration**: Use `atlasexplorer.py` directly in your code
2. **Custom Experiments**: Modify notebook parameters for your workloads  
3. **Batch Processing**: Automated performance regression testing
4. **Research Studies**: Large-scale architecture comparison studies

## 🆘 Troubleshooting & FAQ

### ❓ **Common Issues**

**Q: "No credentials found" error**  
A: Run `uv run atlasexplorer/atlasexplorer.py configure` to set up authentication

**Q: Installation or dependency errors**  
A: The project uses modern `uv` dependency management. Make sure you have `uv` installed and use:
   - `uv sync --group notebooks` (installs everything including Jupyter)
   - `uv run jupyter notebook` (runs Jupyter in the project environment)

**Q: Import errors when running notebooks**  
A: Make sure you installed with notebook support: `uv sync --group notebooks`

**Q: Jupyter notebook won't start**  
A: Use `uv run jupyter notebook` to run within the project environment

**Q: Experiment takes too long**  
A: Multicore experiments take 2-5 minutes. Single-core takes 30-60 seconds.

**Q: API connection errors**  
A: Check your network connection and verify credentials are correct

**Q: Test failures with cycle count mismatches**  
A: Tests use tolerance ranges (±100 cycles) to account for minor simulation variations. Small differences in cycle counts are normal and expected.

**Q: Warnings about "Error processing file entry in ELF" during tests**  
A: These are harmless warnings from the library trying to extract debug information from ELF files. They don't affect performance analysis results. You can reduce verbosity by setting `verbose=False` in your code if desired.

### 🔧 **Performance Tips**

- **Use `development` channel** for testing and learning
- **Start with single-core** experiments to understand basics
- **Compare results** across different optimization levels  
- **Save experiment results** in `myexperiments/` for future reference
- **Use verbose mode** (`--verbose`) for debugging

### 📞 **Getting Help**

- 📖 **Documentation**: This README and notebook tutorials
- 🐛 **Issues**: [GitHub Issues](https://github.com/MIPS/mips-ae-pylib/issues)
- 💬 **Support**: Contact your MIPS representative
- 📧 **Questions**: See inline help in notebooks and CLI tools

## 🏆 Advanced Use Cases

### 📊 **Comparative Studies**

```bash
# Compare compiler optimizations  
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O0.elf --expdir study_O0
uv run examples/ae_singlecore.py --elf resources/mandelbrot_rv64_O3.elf --expdir study_O3

# Compare core counts
uv run examples/ae_multicore.py --core "I8500_(2_threads)" --expdir scaling_2core
uv run examples/ae_multicore.py --core "I8500_(4_threads)" --expdir scaling_4core
```

### 🔄 **CI/CD Integration**

```yaml
# GitHub Actions example
- name: Performance Regression Test
  env:
    MIPS_ATLAS_CONFIG: ${{ secrets.MIPS_ATLAS_CONFIG }}
  run: |
    uv run examples/ae_singlecore.py --elf myapp.elf --expdir ci_results
    # Add performance threshold checking
```

### 🧪 **Custom Analysis**

```python
from atlasexplorer import AtlasExplorer, Experiment

# Custom experiment workflow
ae = AtlasExplorer(channel="development")  
experiment = Experiment("my_analysis", ae)
experiment.addWorkload("my_program.elf")
experiment.setCore("I8500_(1_thread)")
experiment.run()

# Extract specific metrics
summary = experiment.getSummary()
cycles = summary.getTotalCycles()
print(f"Performance: {cycles:,} cycles")
```

## 🌟 Why Choose ATLAS Explorer?

✅ **Accurate Simulation** - Cycle-accurate models of real MIPS hardware  
✅ **Comprehensive Metrics** - 50+ performance indicators and insights  
✅ **Beginner Friendly** - Guided notebooks with educational content  
✅ **Production Ready** - Command-line tools for automation and CI/CD  
✅ **Cloud Powered** - No local setup, instant access to powerful simulation  
✅ **Parallel Analysis** - Advanced multicore and scaling studies  
✅ **Real Results** - Based on actual experimental data and proven methodologies

---

<div align="center">

**🚀 Ready to unlock the secrets of CPU performance?**

[Get Started with Jupyter Notebooks](#-getting-started---choose-your-path) | [Quick CLI Setup](#-command-line-tools-for-automation--cicd) | [View Example Results](#-example-results)

*Built with ❤️ by the MIPS Performance Team*

</div>