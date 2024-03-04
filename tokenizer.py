class BasicTokenizer:
    def merge(self, text, new_pair, new_pair_id):
        new_text = []
        i = 0
        while i < len(text):
            if i < len(text) - 1 and text[i] == new_pair[0] and text[i+1] == new_pair[1]:
                new_text.append(new_pair_id)
                i += 2
            else:
                new_text.append(text[i])
                i += 1
        return new_text

    def get_stats(self, text):
        counts = {}
        for pair in zip(text, text[1:]):
            counts[pair] = counts.get(pair, 0) + 1
        return counts