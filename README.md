# LEVER_IMG
The scheme to enhance security and performance in image deduplication based on lever

## Dependency
### Language
Python: version 3.11.5

### Library
1. numpy: version 1.25.2
2. opencv-python: version 4.8.0.76
3. pycryptodome: version 3.17

### Dataset
1. Unsplash, “+e UNSPLASH Image Database,” 2013, https://www.unsplash.com/.
2. sipi, “+e USC-SIPI Image Database,” 1997, http://sipi.usc.edu/database/.

## Source Code
- img_hidden.py: implement image encrypt and message hidden algorithm.
- performance.py: experiment in performance.
- security.py: experiment in security.

## Experiment
> **Performance**  
> 1. Communication Overhead  
> - Test for 0%, 10%, 20%, ..., 100% images in dataset are uploaded in advance.
> - Compared with LEVER and O-DD.
> 
> 2. Storage Overhead  
> - Test for 0%, 10%, 20%, ..., 100% images in dataset are uploaded in advance.
> - Compared with LEVER and O-DD.
> - Result: Deduplication Rate.

## Output
Base dictionary: **./result**
- Performance Experiment: **$(Base dictionary)/perf/**
- Security Experiment: **$(Base dictionary)/secu/**

## Reference