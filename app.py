import json # parse and build JSON request bodies
import os # read the LLAMA_BASE_URL environment variable
import urllib.request # standard library HTTP client, no requests
import streamlit as st # web UI framework for the chat
def stream_reply(sent_messages): # stream assistant reply from llama server
    """Yield text chunks from the llama.cpp server."""
    body_bytes = json.dumps({"messages": sent_messages, "stream": True}).encode("utf-8") # It turns your Python dict into a JSON string, then into bytes, because urllib sends bytes not text.
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
            chunk_text = json.loads(line_text[5:])["choices"][0].get("delta", {}).get("content") # extract new text from delta, may be None
            if chunk_text: # skip role only and null chunks
                yield chunk_text # send text to Streamlit stream writer
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
        with st.chat_message("assistant"): # container for the streamed reply
            reply_text = st.write_stream(stream_reply(st.session_state.chat_messages)) # show chunks live, return full text
        st.session_state.chat_messages.append({"role": "assistant", "content": reply_text}) # store full reply for next reruns
if __name__ == "__main__": # Streamlit runs the script as main
    main() # start the chat app here