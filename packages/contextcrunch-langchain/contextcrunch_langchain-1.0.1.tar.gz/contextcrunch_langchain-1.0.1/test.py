## Set env vars
from operator import itemgetter

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
from langchain.globals import set_debug

set_debug(True)

from contextcrunch_langchain import ConversationCruncher
load_dotenv()




model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Conversation Summary:\n{history}"),
        ("human", "{input}"),
    ]
)

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("I have a ML api that i would like to monetize, so I want to create an API proxy that will handle users, authentication, signup, and billing. Can I use vercel for this?")
memory.chat_memory.add_ai_message("Yes, you can use Vercel to create an API proxy for your machine learning API that handles user management, authentication, signup, and billing. Vercel is primarily known for its capabilities in deploying and hosting web applications and static sites, but it can also be used for serverless functions, which you can leverage to build your API proxy. Here are some key points to consider when setting up your API proxy on Vercel: Serverless Functions: You can write serverless functions in Vercel to handle various aspects of your API, like user authentication, signup, and billing. These functions can be written in languages like JavaScript, TypeScript, Python, etc. Authentication: For handling user authentication, you can integrate third-party services like Auth0, Firebase Authentication, or build your own custom solution. These services can be integrated into your serverless functions. Database Integration: You'll likely need a database to store user information and other relevant data. Vercel can connect to various databases, and you can choose one based on your requirements. Billing and Subscription Management: For billing, you can use third-party services like Stripe, PayPal, or others. These services offer APIs that you can integrate into your Vercel application to handle subscriptions, one-time payments, and other billing-related activities. API Routing and Proxying: You can set up routes in your Vercel project to manage the requests to your machine learning API. This involves receiving requests, authenticating them, and then forwarding them to your actual ML API. Environment Variables: Vercel supports environment variables, which are essential for securely storing API keys, database connection strings, and other sensitive information. Scalability: Vercel offers good scalability options, which is beneficial if your API usage grows over time. Deployment and CI/CD: Vercel provides easy deployment options and integrates with various version control systems for continuous integration and deployment. When setting up your API proxy on Vercel, you'll need to write the code for the serverless functions, set up the necessary integrations with databases and authentication/billing services, and configure your project's deployment and routing settings. Always ensure to test your setup thoroughly to handle various user scenarios and security considerations.")


chain = (
    {'history': RunnableLambda(memory.load_memory_variables) | itemgetter("history"), 'input': RunnablePassthrough()}
    | ConversationCruncher()
    | prompt
    | model
)


with get_openai_callback() as cb:
    result = chain.invoke("What is my initial goal?")
    print(f'{result}')
    print(f'tokens: {cb}')