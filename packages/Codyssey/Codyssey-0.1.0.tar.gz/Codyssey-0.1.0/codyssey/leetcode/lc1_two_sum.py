"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]
"""
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Given a list of integers nums and an integer target,
        this function returns a list of two indices, i and j
        such that nums[i] + nums[j] equals the target.

        This implementation uses a nested loop to iterate through
        all pairs of numbers in nums and check if their sum equals target.

        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        for i, num in enumerate(nums):
            for j in range(i+1, len(nums)):
                if num + nums[j] == target:
                    return [i, j]

        return []

    def twoSum_hash(self, nums: List[int], target: int) -> List[int]:
        """
        Given a list of integers nums and an integer target,
        this function returns a list of two indices, i and j
        such that nums[i] + nums[j] equals the target.

        This implementation uses a hashmap to store each num as
        a key mapped to its index. It then checks if target - num
        exists in the hashmap in O(1) time.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        _map = {}
        for i, num in enumerate(nums):
            if target - num in _map:
                return [_map[target - num], i]
            _map[num] = i


if __name__ == "__main__":
    nums = [3,4,5,6,7,8,9]
    target = 17
    out = Solution().twoSum_hash(nums, target)
    print(out)
