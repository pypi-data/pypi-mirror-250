"""
Given a string s, find the length of the longest
substring without repeating characters.


Example 1:
    Input: s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with the length of 3.

Example 2:
    Input: s = "bbbbb"
    Output: 1
    Explanation: The answer is "b", with the length of 1.

Example 3:
    Input: s = "pwwkew"
    Output: 3
    Explanation: The answer is "wke", with the length of 3.
    Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:
    0 <= s.length <= 5 * 104
    s consists of English letters, digits, symbols and spaces.

"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Finds the length of the longest substring in the given string s
        that contains no repeating characters.

        Args:
            s (str): The input string

        Returns:
            int: The length of the longest substring with no repeating characters

        Time Complexity: O(n)
        Space Complexity: O(min(m, n)) , where n is the length of the input string, and m is the size of the charset/alphabet.

        """
        seen = {}
        start = result =  0
        for i, _char in enumerate(s):
            if seen.get(_char, -1) >= start:
                start = seen[_char] + 1

            seen[_char] = i
            result = max(result, i-start+1)

        return result


if __name__ == "__main__":
    s = Solution()
    assert(s.lengthOfLongestSubstring("abcabcbb") == 3)
    assert(s.lengthOfLongestSubstring("bbbbb") == 1)
    assert(s.lengthOfLongestSubstring("pwwkew") == 3)