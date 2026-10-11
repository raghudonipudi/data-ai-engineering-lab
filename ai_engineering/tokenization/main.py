import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there, My name is Raghu!"
tokens = enc.encode(text)

print(f"Tokens", tokens)

decoded = enc.decode(tokens)

print(f"Decoded, {decoded}")

