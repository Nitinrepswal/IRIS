import time


def stream_response(response):
    words = response.split()

    for word in words:
        yield word + " "
        time.sleep(0.3)


response = "IRIS is an intelligent AI assistant."

print("Streaming response:\n")

full_response = ""

for chunk in stream_response(response):
    print(chunk, end="", flush=True)
    full_response += chunk

print("\n\nComplete response:")
print(full_response)