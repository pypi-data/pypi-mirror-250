import concurrent.futures
import requests
import os
import time
from dotenv import load_dotenv
from transformers import AutoTokenizer
from typing import  Union

from .deny_list import attack_deny_list 

class PromptChecker():
    def __init__(self):
        load_dotenv()
        self.__API_URL = "https://api.aeglos.ai/api/v1"
        self.__huggingface_key=os.environ.get('AEGLOS_API_KEY')
        self.__headers= {"x-api-key": f"Bearer {self.__huggingface_key}",
                         "Content-Type": "application/json"}

    def spin_up_api(self):
        """
        Spins up the API -> Prevents model loading
        """
        response = requests.post(self.__API_URL, headers=self.__headers, json={"inputs": "spin up sent"})
        print(response.json())

    def query(self, payload, max_retries=5, retry_delay=1)->Union[dict, None]:
        """
        Queries the model, retry until we get something or throw an error.
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.post(self.__API_URL, headers=self.__headers, json=payload)
                val=response.json()
                if isinstance(val, dict) and 'error' in val:
                    raise Exception(val["error"])
                else:
                    return val[0]
            except Exception as e:
                print(f"Request failed: {e}. Retrying...")
                
            time.sleep(retry_delay)
            retry_count += 1

    def contains_known_attack(self, prompt)->bool:
        """
        Calls the query API to check if the prompt looks valid or not!
        """
        prompt = prompt.lower()
        
        for attack in attack_deny_list:
            if attack in prompt:
                return True
    
        output = self.query({"inputs": prompt})
        if not output:
            raise Exception("API Call not working")

        if output["label"]==False:
            return False
    
        return output["score"]>0.7
        
        return malicious_possiblity>=0.5


    def split_prompt(self, prompt, max_tokens = 256): ### OUR MODEL HAS 512
        """
        Splits the prompt into a list of tokens. Makes it so that tokens are self co
        """
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")
        token_chunks = []
        current_chunk = []
        tokens = tokenizer.tokenize(prompt)

        for token in tokens:
            current_chunk.append(token)
            if len(current_chunk) >= max_tokens:
                token_chunks.append(current_chunk)
                current_chunk = []

        if current_chunk:
            token_chunks.append(current_chunk)

        text_chunks = [''.join(tokenizer.decode(tokenizer.convert_tokens_to_ids(chunk), skip_special_tokens=True)) for chunk in token_chunks]
        return text_chunks

    def concurrent_contains_known_attack(self, prompt, max_threads = 4)->bool:
        """
        Splits the prompt into tokens and concurrently checks if each of the tokens contain
        an attack
        """
        text_chunks = self.split_prompt(prompt)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            is_chunk_malicious = executor.map(self.contains_known_attack, text_chunks)
            for malicious in is_chunk_malicious:
                if malicious:
                    return malicious
        return False