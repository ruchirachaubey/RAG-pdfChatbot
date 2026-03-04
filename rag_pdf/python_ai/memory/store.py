from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

def get_config(thread_id):
    return {
        "configurable": {"thread_id": thread_id},
        "metadata": {"thread_id": thread_id},
    }