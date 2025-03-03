from typing import List, Optional, Tuple, Union
import math


def dynamic_multi_way_search(arr: List[int], target: int) -> int:
    """
    A dynamic multi-way search that adjusts the number of divisions based on array size.
    
    Args:
        arr: Sorted array to search in
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
    """
    def calculate_divisions(size: int) -> int:
        """Calculate optimal number of divisions based on array size using logarithmic scaling"""
        # Base case: use binary search for very small arrays
        if size <= 10:
            return 2
            
        # Calculate divisions using logarithmic formula: 2 * log2(size)
        # This gives divisions that grow with array size but not too rapidly
        divisions = int(2 * math.log2(size))
        
        # Ensure divisions is a power of 2 for efficient partitioning
        # (optional, but can help with some hardware optimizations)
        # divisions = 2 ** math.floor(math.log2(divisions))
        
        # Cap at a reasonable maximum to avoid too many comparisons
        return min(divisions, 32)
    
    def search_recursive(left: int, right: int) -> int:
        if left > right:
            return -1  # Element not found
            
        # Calculate current range size
        range_size = right - left + 1
        
        # Dynamically determine number of divisions
        divisions = calculate_divisions(range_size)
        
        # Create division points
        division_points = []
        segment_size = range_size / divisions
        
        for i in range(1, divisions):
            point = left + int(i * segment_size)
            division_points.append(point)
            
            # Check if target is at this division point
            if arr[point] == target:
                return point
        
        # Determine which segment to search next
        for i in range(len(division_points)):
            if target < arr[division_points[i]]:
                if i == 0:
                    return search_recursive(left, division_points[i] - 1)
                else:
                    return search_recursive(division_points[i-1] + 1, division_points[i] - 1)
        
        # If we get here, target must be in the last segment
        return search_recursive(division_points[-1] + 1, right)
    
    return search_recursive(0, len(arr) - 1)


def dynamic_multi_way_search_iterative(arr: List[int], target: int) -> int:
    """
    Iterative version of dynamic multi-way search.
    
    Args:
        arr: Sorted array to search in
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Calculate current range size
        range_size = right - left + 1
        
        # Dynamically determine number of divisions using logarithmic scaling
        if range_size <= 10:
            divisions = 2  # Base case for small arrays
        else:
            # Scale divisions logarithmically with array size
            divisions = int(2 * math.log2(range_size))
            
            # Cap at a reasonable maximum
            divisions = min(divisions, 32)
        
        # Create division points
        division_points = []
        segment_size = range_size / divisions
        
        found_in_division = False
        for i in range(1, divisions):
            point = left + int(i * segment_size)
            if point >= len(arr):  # Safety check
                break
                
            division_points.append(point)
            
            # Check if target is at this division point
            if arr[point] == target:
                return point
        
        # If division points couldn't be created (very small array)
        if not division_points:
            # Fall back to binary search
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
            continue
        
        # Determine which segment to search next
        found_segment = False
        for i in range(len(division_points)):
            if target < arr[division_points[i]]:
                if i == 0:
                    right = division_points[i] - 1
                else:
                    left = division_points[i-1] + 1
                    right = division_points[i] - 1
                found_segment = True
                break
        
        # If target is in the last segment
        if not found_segment:
            left = division_points[-1] + 1
    
    return -1  # Element not found


# Testing function
def test_search(search_func):
    # Test with different sized arrays
    test_cases = [
        (list(range(10)), 5),             # Small array
        (list(range(100)), 42),           # Medium array
        (list(range(1000)), 777),         # Large array
        (list(range(10000)), 9876),       # Very large array
        (list(range(100)), 100),          # Not found case
    ]
    
    for arr, target in test_cases:
        result = search_func(arr, target)
        expected = target if target < len(arr) else -1
        print(f"Array size: {len(arr)}, Target: {target}, Found at: {result}, Expected: {expected}")

if __name__ == "__main__":
    print("Testing recursive implementation:")
    test_search(dynamic_multi_way_search)
    
    print("\nTesting iterative implementation:")
    test_search(dynamic_multi_way_search_iterative)