import os, random, requests, unicodedata
from typing import List, Optional, Tuple
from hashlib import md5

class LanguageDetect:
    def has_chinese(self, text):
        if text is None:
            return False

        for char in text:
            if 'CJK' in unicodedata.name(char, ''):
                return True
        return False

    def filter_texts(self, texts: List[str]) -> Tuple[List[int], List[str]]:
        # 过滤掉中文和空文本
        translate_texts = []
        translate_index = []
        for index, text in enumerate(texts):
            if text is None or len(text) == 0:
                continue
            if self.has_chinese(text):
                continue
            translate_texts.append(text)
            translate_index.append(index)
        return translate_index, translate_texts

class Translator(LanguageDetect):
    retry_times = 3
    url: str = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    app_id: str = os.environ.get("BAIDU_APP_ID") or ""
    app_key: str = os.environ.get("BAIDU_APP_KEY") or ""

    def call(self, texts: List[str], context: Optional[str] = None) -> List[str]:
        texts = [t for t in texts]
        translate_index, translate_texts = self.filter_texts(texts)
        for idx, translate_text in zip(translate_index, translate_texts):
            for i in range(self.retry_times):
                try:
                    r = requests.post(self.url, params=self.build_payload(translate_text), headers=self.headers())
                    result = r.json()
                    if "error_code" in result:
                        raise Exception(result["error_msg"])
                    content = [t["dst"] for t in result["trans_result"]]
                    # 将翻译后的文本填充回去
                    texts[idx] = '\n'.join(map(str, content))

                except Exception as e:
                    print(e)
                    if i < self.retry_times - 1:
                        continue
                break
        return texts

    def make_md5(self, s: str, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def build_payload(self, text: str):
        from_lang = 'en'
        to_lang = 'zh'
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.app_id + text + str(salt) + self.app_key)
        return { 'appid': self.app_id, 'q': text , 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign, 'action': 1 }

    def headers(self):
        return { 'Content-Type': 'application/x-www-form-urlencoded' }

