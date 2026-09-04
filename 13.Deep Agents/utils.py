import json


def format_message_content(message):
    parts = []
    tool_calls_processed = False

    if isinstance(message.content, str):
        parts.append(message.content)
    elif isinstance(message.content, list):
        for item in message.content:
            if item.get("type") == "text":
                parts.append(item["text"])
            elif item.get("type") == "tool_use":
                parts.append(f"\n🔧 Tool Call: {item['name']}")
                parts.append(f"   Args: {json.dumps(item['input'], indent=2, ensure_ascii=False)}")
                parts.append(f"   ID: {item.get('id', 'N/A')}")
                tool_calls_processed = True
    else:
        parts.append(str(message.content))

    if (
            not tool_calls_processed
            and hasattr(message, "tool_calls")
            and message.tool_calls
    ):
        for tool_call in message.tool_calls:
            parts.append(f"\n🔧 Tool Call: {tool_call['name']}")
            parts.append(f"   Args: {json.dumps(tool_call['args'], indent=2, ensure_ascii=False)}")
            parts.append(f"   ID: {tool_call['id']}")

    return "\n".join(parts)


def print_stream_chunk(chunk):
    """
    分类打印 LangGraph 流式输出的节点数据。

    Args:
        chunk: LangGraph stream 返回的单个 chunk
    """
    for node_name, data in chunk.items():

        print(f"\n{'=' * 50}")
        print(f"📌 节点：{node_name}")

        if not data:
            continue

        messages = data.get("messages", [])

        for message in messages:

            # AI 消息
            if message.type == "ai":

                # AI 调用工具
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"🔧 调用工具：{tool_call['name']}")
                        print(f"   参数：{tool_call['args']}")

                # AI 普通回复
                elif message.content:
                    print(f"🤖 AI：{message.content}")

            # Tool 消息
            elif message.type == "tool":
                print(f"🔨 工具结果：{message.name}")
                print(f"   {message.content}")
