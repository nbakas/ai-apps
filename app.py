import json # parse and build JSON request bodies
import os # read the LLAMA_BASE_URL environment variable
import urllib.request # standard library HTTP client, no requests
import streamlit as st # web UI framework for the chat
import time # measure response timing
# For profiling you can use `docker stats`. It shows live CPU %, RAM, network, and disk I/O for each container. Run it in a second terminal while you use the app. It does not show GPU use; use `nvidia-smi` for that.
def stream_reply(sent_messages): # stream assistant reply from llama server
    """Yield text chunks from the llama.cpp server."""
    start_time = time.perf_counter() # record request start time
    first_time = None # store first text arrival
    token_count = 0 # store actual generated token count
    body_bytes = json.dumps({"messages": sent_messages, "stream": True, "stream_options": {"include_usage": True}}).encode("utf-8") # It turns your Python dict into a JSON string, then into bytes, because urllib sends bytes not text.
    post_request = urllib.request.Request(f"{os.environ.get("LLAMA_BASE_URL")}/chat/completions", # build POST to OpenAI compatible endpoint
                                          data=body_bytes, # request body as UTF-8 JSON bytes
                                          headers={"Content-Type": "application/json"}, # tell server body is JSON
                                          method="POST") # send the request as HTTP POST
    no_proxy_opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) # disable environment proxy use
    with no_proxy_opener.open(post_request, timeout=300) as server_reply: # open connection, wait max 300 seconds
        for raw_line in server_reply: # read server sent events line by line
            line_text = raw_line.decode("utf-8").strip() # bytes to text, remove whitespace
            if not line_text.startswith("data:") or line_text.endswith("[DONE]"): # skip blanks and end marker
                continue # go to the next line
            chunk_json = json.loads(line_text[5:]) # parse streamed response
            if chunk_json.get("usage"):
                token_count = chunk_json["usage"].get("completion_tokens", 0) # read server token count
            chunk_text = chunk_json["choices"][0].get("delta", {}).get("content") if chunk_json.get("choices") else None
            if chunk_text:
                if first_time is None:
                    first_time = time.perf_counter()  # monotonic high-resolution timer; time.time() can jump with system clock changes
                yield chunk_text
    if first_time is not None:
        total_time = time.perf_counter() - start_time # measure complete response duration
        generation_time = time.perf_counter() - first_time # measure generation duration after first text
        tps = max(token_count - 1, 0) / generation_time if generation_time > 0 else 0 # calculate token generation rate
        st.caption(f"TTFT: {first_time - start_time:.2f}s | TPS: {tps:.1f} | Total time: {total_time:.2f}s | Total tokens: {token_count}" if token_count else f"TTFT: {first_time - start_time:.2f}s | Total time: {total_time:.2f}s | Tokens: N/A")
def main(): # build and run the chat page
    st.title("Local LLM Chat") # page heading shown at the top
    if "chat_messages" not in st.session_state: # session state, no streamlit cache
        st.session_state.chat_messages = [] # start with empty chat history
    for past_message in st.session_state.chat_messages: # redraw history on every rerun
        st.chat_message(past_message["role"]).markdown(past_message["content"]) # show one stored message with role
    user_text = st.chat_input("Ask something") # input box, returns text or None
    if user_text: # run only when user sends text
        st.session_state.chat_messages.append({"role": "user", "content": user_text}) # store user message in history
        st.chat_message("user").markdown(user_text) # show the user message right away
        with st.chat_message("assistant"):
            reply_text = st.write_stream(stream_reply(st.session_state.chat_messages)) # show chunks live, return full text
        st.session_state.chat_messages.append({"role": "assistant", "content": reply_text}) # store full reply for next reruns
if __name__ == "__main__": # Streamlit runs the script as main
    main() # start the chat app here