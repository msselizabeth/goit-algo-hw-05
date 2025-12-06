def binary_search(nums, target) -> int:
    attempts = 0
    min = 0
    max = len(nums) - 1
    upper_value = None

    while min < max:
        attempts += 1
        mid = (min + max) // 2
        guess = nums[mid]
        
        if guess < target:
            min = mid + 1

        else:
            upper_value = guess
            max = mid - 1
    
    return(attempts, upper_value)


a, m = binary_search([0.99, 1.25, 3.33, 4.57, 5.78, 7.11, 9.05], 3.58)
print(f"Attempts: {a}")
print(f"Closest value: {m}")


