# Example usage and testing
from mooonpy.tools.loop_utils import Cartesian
from mooonpy import Path
import os
print("=" * 80)
print("CARTESIAN PRODUCT GENERATOR - COMPREHENSIVE EXAMPLES")
print("=" * 80)

# Example 1: Basic Usage with Mixed Data Types
print("\n1. BASIC USAGE - Mixed data types and automatic iteration")
print("-" * 60)

basic_sets = {
    'material': ['steel', 'aluminum'],  # List of strings
    'material.ele':['Fe','Al'], # element symbols
    'size': range(10, 21, 10),  # Range object (10, 20)
    'temp': [300, 400],  # List of numbers
    'active': [True, False]  # Boolean values
}

basic_cart = Cartesian(basic_sets)
print(f"Total combinations: {len(basic_cart)}")
print(f"Dimension structure: {basic_cart.dimension_sizes}")

print("\nFirst 5 combinations:")
for i, result in enumerate(basic_cart.generate()):
    if i >= 5:
        break
    print(f"  {i + 1}: {dict(result)}")

# Example 2: Index Tracking and Access
print("\n2. INDEX TRACKING - Global and per-dimension indices")
print("-" * 60)

index_sets = {
    'R': ['01', '02', '03'],
    'direction': ['x', 'y', 'z'],
    'param': ['A', 'B']
}

index_cart = Cartesian(index_sets)

print("All combinations with index information:")
for result in index_cart.generate():
    print(f"  Global #{result.global_idx}: {dict(result)}")
    print(f"    Dimension indices: {result.dimension_indices}")

# Example 3: Combined Indices for Multi-dimensional Analysis
print("\n3. COMBINED INDICES - Multi-dimensional indexing")
print("-" * 60)

# Request combined indices for R+direction pair
print("With combined R+direction index:")
for result in index_cart.generate(return_combined_indices=[('R', 'direction')]):
    r_dir_idx = result.combined_indices[('R', 'direction')]
    print(f"  {dict(result)} -> R+direction index: {r_dir_idx}")

# Multiple combined indices
print("\nMultiple combined indices (R+direction, direction+param):")
for i, result in enumerate(index_cart.generate(
        return_combined_indices=[('R', 'direction'), ('direction', 'param')]
)):
    if i >= 3:  # Show only first 3 for brevity
        break
    print(f"  {dict(result)}")
    print(f"    R+direction: {result.combined_indices[('R', 'direction')]}")
    print(f"    direction+param: {result.combined_indices[('direction', 'param')]}")
print('...')

# Example 4: Reverse Index Lookup
print("\n4. REVERSE LOOKUP - Find indices from values")
print("-" * 60)

sample_values = {'R': '02', 'direction': 'z', 'param': 'A'}
combined_idx = index_cart.get_combined_index(('R', 'direction'), sample_values)
print(f"Values: {sample_values}")
print(f"Combined R+direction index: {combined_idx}")

# Example 5: String and Path Formatting
print("\n5. STRING/PATH FORMATTING - Template processing")
print("-" * 60)

file_sets = {
    'experiment': ['exp1', 'exp2'],
    'material': ['steel', 'Al'],
    'replicate': ['r1', 'r2']
}

file_cart = Cartesian(file_sets)

# Single string formatting
template_str = "data/{experiment}/{material}_rep{replicate}.txt"

# Path object formatting (Path inherits from str with os.path operations)
template_path = Path("results/{experiment}/analysis_{material}_{replicate}.csv")

# Dictionary of templates
template_dict = {
    'input': Path("input/{experiment}/{material}_{replicate}.dat"),
    'output': "output_{experiment}_{material}_{replicate}.log",
    'backup': Path("backup/{experiment}")
}

print("Template formatting examples:")
for i, result in enumerate(file_cart.generate()):
    if i >= 3:  # Show first 3
        break
    print(f"\n  Combination {i + 1}: {dict(result)}")
    print(f"    String: {result.string_format(template_str)}")
    print(f"    Path: {result.string_format(template_path)}")  # Returns Path object

    formatted_dict = result.string_format(template_dict)
    print(f"    Dict templates:")
    for key, path in formatted_dict.items():
        print(f"      {key}: {path} {'(Path)' if isinstance(path, Path) else '(str)'}")
print('...')

# Example 6: Conditional Dimensions - Advanced Feature
print("\n6. CONDITIONAL DIMENSIONS - Context-dependent values")
print("-" * 60)

# Key format: "dimension.condition.name"
# When dimension index == condition, the conditional value is included
conditional_sets = {
    'mode': ['basic', 'advanced', 'expert'],  # Base dimension (0, 1, 2)
    'mode.0.settings': ['default'],  # Only when mode index = 0 (basic)
    'mode.1.settings': ['optimized', 'balanced'],  # Only when mode index = 1 (advanced)
    'mode.2.settings': ['custom', 'extreme'],  # Only when mode index = 2 (expert)
    'version': ['v1', 'v2'],  # Independent dimension
}

cond_cart = Cartesian(conditional_sets)
print(f"Total conditional combinations: {len(cond_cart)}")

print("\nConditional combinations (first 8):")
for i, result in enumerate(cond_cart.generate()):
    if i >= 8:
        break
    mode_val = result['mode']
    settings_val = result.get('settings', 'N/A')
    print(f"  {i + 1}: mode={mode_val}, settings={settings_val}, "
          f"version={result['version']}")
print('...')

# Example 7: Complex Conditional with Multiple Triggers
print("\n7. COMPLEX CONDITIONALS - Multiple conditions per dimension")
print("-" * 60)

complex_sets = {
    'algorithm': ['A', 'B', 'C'],  # Base: 0, 1, 2
    'algorithm.0.param': ['alpha', 'beta'],  # A gets param alpha/beta
    'algorithm.1.param': ['gamma'],  # B gets param gamma
    'algorithm.2.param': ['delta', 'epsilon'],  # C gets param delta/epsilon
    'algorithm.1.special': ['turbo', 'ultra'],  # B also gets special mode. Not sure if I like this behavior, but also do not see a use for it
    'algorithm.cost':[5,10,20], # Base parallel dim
    'dataset': ['small', 'large']  # Independent
}

complex_cart = Cartesian(complex_sets)
print(f"Complex conditional combinations: {len(complex_cart)}")

print("\nAll complex conditional combinations:")
for i, result in enumerate(complex_cart.generate()):
    alg = result['algorithm']
    cost = result['cost']
    param = result.get('param', 'none')
    special = result.get('special', 'none')
    dataset = result['dataset']
    print(f"  {i + 1}: {alg}/{cost}+ {param} + special:{special} + {dataset}")

# Example 8: Edge Cases and Error Handling
print("\n8. EDGE CASES - Boundary conditions and error handling")
print("-" * 60)

# Single value dimensions
single_sets = {
    'constant': ['only_value'],  # Single item list
    'single_num': [42],  # Single number in list
    'single_str': 'a',  # Single string NOT converted to list.
    # 'foo' is equivalent to ['f','o','o']
    'single_range': range(5, 6)  # Range with one value
}

single_cart = Cartesian(single_sets)
print(f"Single-value dimensions: {len(single_cart)} combination(s)")

for result in single_cart.generate():
    print(f"  Result: {dict(result)}")

# Empty dimension handling (this would raise an error)
print("\nError handling examples:")
try:
    error_sets = {'empty': []}  # Empty list
    error_cart = Cartesian(error_sets)
    print("  Empty dimension created successfully")
except Exception as e:
    print(f"  Empty dimension error: {e}")

# Missing base dimension for conditional
try:
    missing_base = {
        'missing.0.value': ['test']  # Conditional without base
    }
    missing_cart = Cartesian(missing_base)
except ValueError as e:
    print(f"  Missing base dimension error: {e}")

# Invalid combined index request
try:
    basic_cart.get_combined_index(('nonexistent',), {'material': 'steel'})
except ValueError as e:
    print(f"  Invalid dimension error: {e}")

# Example 9: Performance and Memory Considerations
print("\n9. PERFORMANCE - Large dimension sets")
print("-" * 60)

large_sets = {
    'batch': range(10),  # 10 values
    'config': range(5),  # 5 values
    'run': range(3)  # 3 values
}
# Total: 10 * 5 * 3 = 150 combinations

large_cart = Cartesian(large_sets)
print(f"Large set total combinations: {len(large_cart)}")

# Using generator (memory efficient)
print("Generator approach (memory efficient):")
count = 0
for result in large_cart.generate():
    count += 1
    if count <= 3:
        print(f"  Sample {count}: {dict(result)}")
    elif count == len(large_cart):
        print(f"  ...and {count - 3} more combinations processed")

# Using list generation (loads all into memory)
print("List approach (loads all combinations):")
all_results = large_cart.generate_list()
print(f"  Generated list with {len(all_results)} CartesianResult objects")

print("\n" + "=" * 80)
print("END OF EXAMPLES")
print("=" * 80)
os.system("pause") ## Keep popup open