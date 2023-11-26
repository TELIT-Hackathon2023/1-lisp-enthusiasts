from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bs4 import BeautifulSoup

from .serializers import AnalyticsInputSerializer, PersonaInputSerialier
from .services import get_text_from_website, parse_json, get_web_type_from_users, get_color_contrast, get_dominant_colors
from config.settings import client

import requests
import os, io, json


from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter


class HelloWorldView(APIView):
    def get(self, request):
        data = {'message': 'Hello, World!'}
        return Response(data)


class AnalyticsView(APIView):
    def post(self, request):
        serializer = AnalyticsInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        analytics = os.environ.get('ANALYTICS')
        url = serializer.validated_data['url']
        r = requests.get(analytics + '=' + url)
        final = r.json()

        parsed_data = parse_json(final)

        with io.open('./text_files/data.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(parsed_data, ensure_ascii=False))

        with io.open('./text_files/data.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(parsed_data, ensure_ascii=False))

        return Response(parsed_data, status=status.HTTP_200_OK)


class PersonaView(APIView):
    def post(self, request):
        serializer = PersonaInputSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        res = get_text_from_website(url, url, set())

        res = res[:9000]

        messages = [
            {"role": "system", "content": res},
            {"role": "user", "content": "This is a text content of a website. I want to learn who is the website adressed to. Write a list of personas that the website was created for. For each persona write the name followed by three underscores followed by a short description"}
        ]

        response = client.chat.completions.create(
            model='gpt-4-1106-preview',
            messages=messages
        )

        ans = response.choices[0].message.content.split('\n')

        response = {}

        for elm in ans:
            if len(elm) > 3:
                values = elm.split('___')
                response[values[0]] = values[1]

        type = get_web_type_from_users(response)

        with io.open('./text_files/personas.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({"response": response, "type": type}, ensure_ascii=False))

        return Response({"response": response, "type": type})



class CleanHTMLAPIView(APIView):
    def post(self, request):
        serializer = PersonaInputSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = requests.get(serializer.validated_data['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        cleaned_html = soup.prettify()

        with io.open('./text_files/html.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(cleaned_html, ensure_ascii=False))

        with io.open('./text_files/html.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(cleaned_html, ensure_ascii=False))

        return Response(cleaned_html)


class ContrastAPIView(APIView):
    def post(self, request):
        serializer = PersonaInputSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']

        colors = get_dominant_colors('./screenshot.png')
        contrast = get_color_contrast(colors[0], colors[1])

        return Response({"contrast": contrast})


class TipstAPIView(APIView):
    def get(self, request):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 200,
            chunk_overlap  = 20,
            length_function = len,
            is_separator_regex = False,
        )

        #os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

        #loader = TextLoader('./data.txt')
        #loader_html = TextLoader('./html.txt')
        loader = DirectoryLoader('./text_files', glob="*", loader_cls=TextLoader, recursive=True)

        documents = loader.load()
        embeddings = OpenAIEmbeddings()
        doc = text_splitter.split_documents(documents)
        db = Chroma.from_documents(doc,embeddings, persist_directory="./chroma_db")


        # index = VectorstoreIndexCreator().from_loaders(documents)
        # print(db)

        #print(db.similarity_search("count number of files you received", k=10))
        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={'k':5, 'fetch_k': 50}
        )

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        llm = ChatOpenAI(
            model_name="gpt-4-1106-preview",
            temperature=0)

        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | llm
            | StrOutputParser()
        )

        query = "Are there any potential options to improve website performance ?"
        res = chain.invoke(query)

        with io.open('./tips/tips.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(res, ensure_ascii=False))

        return Response(res)
        