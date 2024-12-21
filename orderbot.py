from openai import OpenAI
import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

class StarbucksChatbot:
    def __init__(self):
        self.message_history = []

    async def ask_openai(self, prompt):
        try:
            # Initialize conversation with system prompt if it's the first message
            if not self.message_history:
                system_prompt = "스타벅스 채팅봇 역할로 고객 질문에 답변하세요. 먼저 고객을 환영하며 시작해주세요."
                self.message_history.append({
                    "role": "system",
                    "content": system_prompt
                })

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.message_history
                )
                print("resetChatting systemPrompt = ", response.choices[0].message.content.strip())
                return response.choices[0].message.content.strip()

            # Add user input to message history after null check
            if prompt:
                self.message_history.append({
                    "role": "user",
                    "content": prompt
                })
            else:
                raise ValueError("사용자 입력이 null입니다.")

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.message_history
            )

            # Extract AI response
            ai_response = response.choices[0].message.content.strip()

            # Add response to message history
            self.message_history.append({
                "role": "assistant",
                "content": ai_response
            })

            return ai_response

        except Exception as error:
            return f"오류 발생: {str(error)}"

    async def handle_input(self, user_input):
        if any(word in user_input.lower() for word in ["안녕", "종료", "끝"]):
            print("봇: 스타벅스를 방문해 주셔서 감사합니다! 좋은 하루 되세요!")
            return True  # Signal to end the conversation
        
        response = await self.ask_openai(user_input)
        print(f"봇: {response}")
        return False  # Continue the conversation

async def main():
    chatbot = StarbucksChatbot()
    
    # Initialize conversation with empty prompt
    initial_response = await chatbot.ask_openai("")
    print(f"봇: {initial_response}")

    while True:
        user_input = input("고객: ")
        should_end = await chatbot.handle_input(user_input)
        if should_end:
            break

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())