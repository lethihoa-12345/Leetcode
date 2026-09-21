class Solution:
    def resultArray(self, nums, k):
        ans = [0] * k
        dp = [0] * k

        for num in nums:
            new_dp = [0] * k
            x = num % k

            # Subarray chỉ gồm num
            new_dp[x] += 1

            # Nối num vào các subarray trước đó
            for r in range(k):
                if dp[r] > 0:
                    new_r = (r * x) % k
                    new_dp[new_r] += dp[r]

            dp = new_dp

            # Cộng tất cả subarray kết thúc tại vị trí hiện tại
            for r in range(k):
                ans[r] += dp[r]

        return ans