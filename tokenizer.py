import unicodedata


class BasicTokenizer:
    def train(self, text, vocab_size, verbose=False):
        merges_num = vocab_size - 256
        text_bytes =  self.encode_to_utf8_list(text)
        self.merges = {}
        self.vocab = {token_value: bytes([token_value]) for token_value in range(256)} 

        for i in range(merges_num):
            text_bytes, most_occuring_pair, token_value = self.train_step(text_bytes, i)
            self.update_tokenizer_dicts(most_occuring_pair, token_value)
            if verbose:
                print(f"Merging {most_occuring_pair} into a new token {token_value}")

    def encode_to_utf8_list(self, text):
        return list(text.encode("utf-8"))

    def train_step(self, text_bytes, index):
        stats = self.get_stats(text_bytes)
        most_occuring_pair = max(stats, key=stats.get)
        token_value = 256 + index
        text_bytes_updated = self.merge(text_bytes, most_occuring_pair, token_value)
        return text_bytes_updated, most_occuring_pair, token_value
        
    def update_tokenizer_dicts(self, most_occuring_pair, token_value):
        self.merges[most_occuring_pair] = token_value
        self.vocab[token_value] = self.vocab[most_occuring_pair[0]] + self.vocab[most_occuring_pair[1]]

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
    
    def encode(self, text):
        ids = self.encode_to_utf8_list(text)
        while len(ids) >= 2:
            pair = self.lowest_merge_index(ids)
            if pair not in self.merges:
                break 
            idx = self.merges[pair]
            ids = self.merge(ids, pair, idx)
        return ids
    
    def lowest_merge_index(self, ids):
        stats = self.get_stats(ids)
        pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
        return pair

    def decode (self, ids):
        text_bytes = b"".join(self.vocab[token_value] for token_value in ids)
        text = text_bytes.decode("utf-8", errors="replace")
        return text