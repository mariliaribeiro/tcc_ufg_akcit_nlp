from dataclasses import dataclass, field
from typing import List, Tuple, Union

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
    ("===============", "Heading level 1"),
    ("---------------", "Heading level 2")
]

@dataclass
class ChunksFromMarkdow:
    source_document: Union[str, List[Document]]
    chunk_size: int = 400
    chunk_overlap: int = 100
    headers_to_split_on: List[Tuple[str, str]] = field(default_factory=lambda: HEADERS_TO_SPLIT_ON)
    
    md_header_splits: list = field(init=False, default_factory=list)
    chunk_documents: list = field(init=False, default_factory=list)

    def __post_init__(self):
        markdown_documents = []
        if isinstance(self.source_document, str):
            markdown_documents.append(self.source_document)
        elif isinstance(self.source_document, list) and all(isinstance(i, Document) for i in self.source_document):
            markdown_documents = [i.page_content for i in self.source_document]
        else:
            markdown_documents = self.source_document


        print(markdown_documents)
        for markdown_document in markdown_documents:
            self.md_header_splits.extend(self.get_md_header_splits(markdown_document))
            self.chunk_documents.extend(self.get_chunk_documents(self.md_header_splits))

    def get_md_header_splits(self, markdown_document: str) -> List[Document]:
        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on, 
            strip_headers=False
        )
        return markdown_splitter.split_text(markdown_document)

    def get_chunk_documents(self, md_header_splits: List[Document]) -> List[Document]:
        # Char-level splits        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # Split chunk documents
        return text_splitter.split_documents(md_header_splits)