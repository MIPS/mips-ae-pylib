# Baseline Comparison

| Metric | New | Baseline | Δ | Δ% |
|--------|----|----------|---|----|
| Total Cycles Consumed | 2.527e+05 | 2.752e+05 | -2.254e+04 | -8.19% |
| Total Instructions Retired (All Threads) | 2.377e+05 | 3.933e+05 | -1.555e+05 | -39.55% |
| Instructions Retired Thread 0 | 1.966e+05 | 1.966e+05 | +0 | +0.00% |
| Instructions Retired Thread 1 | 4.11e+04 | 1.966e+05 | -1.555e+05 | -79.10% |
| Instructions Per Cycle (IPC) | 0.9409 | 1.429 | -0.488 | -34.16% |
| Instruction Per Cycle Thread 0 | 0.7782 | 0.7144 | +0.06375 | +8.92% |
| Instruction Per Cycle Thread 1 | 0.5435 | 0.7153 | -0.1718 | -24.02% |
| ROB Flushes (mispredicts, exceptions, hazards) | 1 | 1 | +0 | +0.00% |
| Total Number of Predictions | 1.21e+04 | 1.213e+04 | -24 | -0.20% |
| Total Number of Predictions Thread 0 | 6063 | 6063 | +0 | +0.00% |
| Total Number of Predictions Thread 1 | 6039 | 6063 | -24 | -0.40% |
| Total Number of No Predictions | 0 | 0 | +0 | +inf% |
| Total Number of No Predicts Thread 0 | 0 | 0 | +0 | +inf% |
| Total Number of No Predicts Thread 1 | 0 | 0 | +0 | +inf% |
| Total Number of Mispredicts | 370 | 307 | +63 | +20.52% |
| Total Number of Mispredicts for Thread 0 | 237 | 139 | +98 | +70.50% |
| Total Number of Mispredicts for Thread 1 | 133 | 168 | -35 | -20.83% |
| Total Mispredicts Per 1K Instructions | 1.195 | 0.7324 | +0.4623 | +63.13% |
| Total Mispredicts Per 1K Instructions Thread 0 | 0.7273 | 0.6612 | +0.06612 | +10.00% |
| Total Mispredicts Per 1K Instructions Thread 1 | 3.431 | 0.8036 | +2.627 | +326.94% |
| ICache Hits | 1.324e+05 | 2.188e+05 | -8.638e+04 | -39.49% |
| ICache Misses | 142 | 89 | +53 | +59.55% |
| ICache Hit Percent | 99.89 | 99.96 | -0.0665 | -0.07% |
| TLB Hits | 1.325e+05 | 2.188e+05 | -8.633e+04 | -39.45% |
| TLB Misses | 2 | 2 | +0 | +0.00% |
| TBL Hit Percent | 100 | 100 | -0.0006 | -0.00% |
| Number of Bonded Loads | 8933 | 1.764e+04 | -8712 | -49.37% |
| Number of Bonded Stores | 8995 | 1.768e+04 | -8684 | -49.12% |
| Number of Misaligned Bonded Loads | 3 | 2 | +1 | +50.00% |
| Number of Misaligned Bonded Stores | 1 | 2 | -1 | -50.00% |
| Misaligned Loads | 0 | 0 | +0 | +inf% |
| Misaligned Stores | 0 | 0 | +0 | +inf% |
| Number of Good Load Bonds | 8930 | 1.764e+04 | -8713 | -49.39% |
| Number of Good Store Bonds | 8994 | 1.768e+04 | -8683 | -49.12% |
| Number of Bad Load Bonds | 3 | 2 | +1 | +50.00% |
| Number of Bad Store Bonds | 1 | 2 | -1 | -50.00% |
| Percentage of Good Load Bonds | 2.977e+05 | 8.822e+05 | -5.845e+05 | -66.26% |
| Percentage of Good Store Bonds | 8994 | 8838 | +155.5 | +1.76% |
| Number of LS Replays (Flushes) | 295 | 297 | -2 | -0.67% |
| Level 1 Data Cache hits | 7.833e+04 | 1.521e+05 | -7.378e+04 | -48.51% |
| Level 1 Data Cache Misses | 236 | 220 | +16 | +7.27% |
| Level 1 Data Cache Hit Percent | 99.7 | 99.86 | -0.156 | -0.16% |
| Level 1 Data Cache Hits Within a Demand | 7.833e+04 | 1.521e+05 | -7.378e+04 | -48.51% |
| Data Translation Lookaside Buffer (DTLB) Hits | 7.856e+04 | 1.523e+05 | -7.377e+04 | -48.43% |
| Data Translation Lookaside Buffer (DTLB) Misses | 14 | 12 | +2 | +16.67% |
| Fixed Page Size Translation Lookaside Buffer (FTLB) Hits | 0 | 0 | +0 | +inf% |
| Fixed Page Size Translation Lookaside Buffer (FTLB) Misses | 0 | 0 | +0 | +inf% |
| Variable Page Size Translation Lookaside Buffer (VTLB) Hits | 2 | 2 | +0 | +0.00% |
| Variable Page Size Translation Lookaside Buffer (VTLB) Misses | 14 | 12 | +2 | +16.67% |
| Level 2 Translation Lookaside Buffer (L2TLB) Hits | 2 | 2 | +0 | +0.00% |
| Level 2 Translation Lookaside Buffer (L2TLB) Misses | 14 | 12 | +2 | +16.67% |
| ALU Stalled, ALU Not Ready | 937 | 2491 | -1554 | -62.38% |
| ALU Stalled, ALU Ops Not Ready | 1.326e+05 | 1.66e+05 | -3.343e+04 | -20.13% |
| Instructions Executed on ALU 0 | 2.293e+04 | 2.858e+04 | -5649 | -19.77% |
| Instructions Executed on ALU 1 | 5.783e+04 | 1.016e+05 | -4.382e+04 | -43.11% |
| Instrution Executed on FPU 0 | 3.143e+04 | 3.436e+04 | -2931 | -8.53% |
| Instrution Executed on FPU 1 | 1.729e+04 | 1.748e+04 | -190 | -1.09% |
| LSU Stall None (cycles) | 0 | 0 | +0 | +inf% |
| Load Queue Full Stall (Cycles) | 0 | 0 | +0 | +inf% |
| Store Queue Full Stall (Cycles) | 0 | 0 | +0 | +inf% |
| Message Queue Full Stall (cycles) | 0 | 0 | +0 | +inf% |
| CPI | 1.063 | 0.6998 | +0.363 | +51.87% |
| Branch Prediction Accuracy % | 96.94 | 97.47 | -0.5256 | -0.54% |
| ICache Miss Rate % | 0.1072 | 0.04067 | +0.06649 | +163.48% |
| DCache Miss Rate % | 0.3004 | 0.1444 | +0.156 | +108.00% |
| DTLB Miss Rate % | 0.01782 | 0.007877 | +0.009941 | +126.20% |
| Load Bond Success % | 99.97 | 99.99 | -0.02225 | -0.02% |
| Store Bond Success % | 99.99 | 99.99 | +0.0001956 | +0.00% |
| Thread Balance % | 130.8 | 0 | +130.8 | +inf% |
| ALU Instruction Mix % | 62.37 | 71.53 | -9.155 | -12.80% |
| FPU Instruction Mix % | 37.63 | 28.47 | +9.155 | +32.15% |