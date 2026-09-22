class Solution:
    def resultArray(self, nums, k, queries):

        n = len(nums)

        # Kích thước Segment Tree
        size = 1
        while size < n:
            size <<= 1

        # product[node] = product của toàn đoạn % k
        product = [1] * (2 * size)

        # prefix[node * k + r]
        prefix = [0] * (2 * size * k)

        # -------------------------
        # Build leaves
        # -------------------------
        for i in range(n):
            p = size + i
            r = nums[i] % k

            product[p] = r
            prefix[p * k + r] = 1

        # -------------------------
        # Merge node
        # -------------------------
        def pull(p):
            left = p << 1
            right = left | 1

            lp = product[left]

            product[p] = (lp * product[right]) % k

            base = p * k
            left_base = left * k
            right_base = right * k

            # Prefix nằm hoàn toàn bên trái
            for r in range(k):
                prefix[base + r] = prefix[left_base + r]

            # Prefix đi qua cả trái và phải
            for r in range(k):
                new_r = (lp * r) % k
                prefix[base + new_r] += prefix[right_base + r]

        # -------------------------
        # Build
        # -------------------------
        for p in range(size - 1, 0, -1):
            pull(p)

        # -------------------------
        # Point Update
        # -------------------------
        def update(index, value):

            p = size + index
            r = value % k

            product[p] = r

            base = p * k

            for x in range(k):
                prefix[base + x] = 0

            prefix[base + r] = 1

            p >>= 1

            while p:
                pull(p)
                p >>= 1

        # -------------------------
        # Range Query [start, n)
        # -------------------------
        def query(start):

            left = size + start
            right = size + n

            # Các node của đoạn query
            left_nodes = []
            right_nodes = []

            while left < right:

                if left & 1:
                    left_nodes.append(left)
                    left += 1

                if right & 1:
                    right -= 1
                    right_nodes.append(right)

                left >>= 1
                right >>= 1

            # Phải xử lý theo thứ tự từ trái -> phải
            nodes = left_nodes + right_nodes[::-1]

            # Kết quả tạm thời
            result = [0] * k

            first = True
            current_product = 1

            for p in nodes:

                base = p * k

                # Node đầu tiên
                if first:

                    for r in range(k):
                        result[r] = prefix[base + r]

                    current_product = product[p]
                    first = False

                    continue

                # Merge:
                # current segment + node hiện tại

                old = result[:]

                for r in range(k):
                    result[r] = old[r]

                for r in range(k):
                    new_r = (current_product * r) % k
                    result[new_r] += prefix[base + r]

                current_product = (
                    current_product * product[p]
                ) % k

            return result

        # -------------------------
        # Process queries
        # -------------------------
        answer = []

        for index, value, start, x in queries:

            # Update tồn tại cho những query sau
            update(index, value)

            # Lấy đoạn [start ... n-1]
            res = query(start)

            answer.append(res[x])

        return answer