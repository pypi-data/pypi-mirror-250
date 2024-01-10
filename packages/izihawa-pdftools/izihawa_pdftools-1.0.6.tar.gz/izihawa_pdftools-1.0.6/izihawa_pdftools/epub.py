import re
import tempfile

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), "lxml")
    text = [para.get_text().strip() for para in soup.find_all("p")]
    text = "\n".join(text)
    text = re.sub("\n([a-z])", r' \g<1>', text)
    return text.strip()


def extract_epub(content: bytes):
    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as t_file:
        t_file.write(content)
        file_name = t_file.name
        book = epub.read_epub(file_name)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        texts = []
        for item in items:
            if "chapter" in item.get_name():
                texts.append(chapter_to_str(item))
        return "\n\n".join(texts)
