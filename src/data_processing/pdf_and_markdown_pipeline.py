from dataclasses import dataclass, field
import logging
from pathlib import Path
import time
from typing import List, Tuple, Union

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
import spacy

from src.data_processing.chunks import HEADERS_TO_SPLIT_ON, ChunksFromMarkdow

nlp = spacy.load("pt_core_news_md")

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)  # Initialize the logger here


@dataclass
class PdfAndMarkdownPipeline:
    """
    Classe responsável por realizar todo o tratamento dos dados de arquivos pdfs e/ou markdown.
    """

    md_documents: List[Document] = field(init=False, default=None)
    chunk_documents: list = field(init=False, default_factory=list)
    chunk_object: ChunksFromMarkdow = field(init=False, default=None)

    def pdf_to_markdown(
        self,
        source_file_path: Union[str, Path],
        dest_dir_path: Union[str, Path]
    ):
        """
        Função responsável por converter arquivos pdf em markdown.

        Args:
            source_file_path (Union[str, Path]): Caminho do arquivo pdf de origem.
            dest_dir_path (Union[str, Path]): Caminho do diretório em que o arquivo markdown gerado deve ser armazenado.
        """
        
        if isinstance(source_file_path, str):
            source_file_path = Path(source_file_path) 
        if isinstance(dest_dir_path, str):
            dest_dir_path = Path(dest_dir_path) 

        conv_result = self.docling_converter(source_file_path)
        if conv_result and conv_result.document:
            text = self.extract_text_from_docling_document(conv_result.document)
            self.save_text_on_md_file(text, source_file_path.name, dest_dir_path)
        else:
            _log.error("Docling conversion failed or returned an empty document.")

        return self


    def docling_converter(self, source_file_path: Path):
        """
        Função responsável pela conversão do arquivo pdf em texto utilizando o docling.

        Args:
            source_file_path (Path): Caminho do arquivo pdf de origem.

        Returns:
            Docling: Objeto do docling que contém o texto do pdf.
        """
        ###########################################################################
        # Docling Parse with EasyOCR
        # ----------------------
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        # pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
        # pipeline_options.generate_page_images = True
        # pipeline_options.generate_picture_images = True
        
        pipeline_options.ocr_options.lang = ["pt", "en", "es",]
        pipeline_options.accelerator_options = AcceleratorOptions(
            num_threads=4, device=AcceleratorDevice.AUTO
        )

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        ###########################################################################

        start_time = time.time()
        conv_result = doc_converter.convert(source_file_path)
        end_time = time.time() - start_time

        _log.info(f"Document {source_file_path} converted in {end_time:.2f} seconds.")
        
        return conv_result


    def extract_text_from_docling_document(self, docling_document) -> str:
        """
        Função que extrai o conteúdo texto do objeto de documento do Docling.

        Args:
            docling_document (Docling): objeto de documento do Docling

        Returns:
            Texto do pdf em formato markdown.
        """
        return docling_document.export_to_text()

    def save_text_on_md_file(self, text: str, file_name: str, dest_dir_path: Path):
        """
        Função responsável por salvar o texto extraído do pdf em arquivo markdown.

        Args:
            text (str): Texto em formato markdown.
            file_name (str): Nome do arquivo.
            dest_dir_path (Path):  Caminho do diretório em que o arquivo markdown gerado deve ser armazenado.
        """

        file_path = dest_dir_path.joinpath(f"{file_name}.md")
        with open(file_path, "w") as f:
            f.write(text)
        
        _log.info(f"Document {file_path} saved.")
        return self

    def load_markdown(self,
        source_file_path: Union[str, Path],
    ):
        """
        Função responsável por carregar o conteúdo do arquivo markdown.

        Args:
            source_file_path (Union[str, Path]): Caminho do arquivo markdown de origem.
         
        """

        if isinstance(source_file_path, str):
            source_file_path = Path(source_file_path) 

        md_loader = UnstructuredMarkdownLoader(source_file_path)
        self.md_documents = md_loader.load()
        _log.info(f"Document {source_file_path} loaded.")
        return self

    def get_chunks(
            self,
            chunk_size: int = 400,
            chunk_overlap: int = 100,
            headers_to_split_on: List[Tuple[str, str]] = field(default_factory=lambda: HEADERS_TO_SPLIT_ON),
    ):
        """
        Função responsável por gerar os chunks a partir do conteúdo de texto do markdown.

        Args:
            chunk_size (int, optional): Tamanho dos chunks. Defaults to 400.
            chunk_overlap (int, optional): Tamanho da sobreposição entre os chunks. Defaults to 100.
            headers_to_split_on (_type_, optional): Lista de cabeçalhos utilizados para gerar os chunks. Defaults to field(default_factory=lambda: HEADERS_TO_SPLIT_ON).
        """

        self.chunk_object = ChunksFromMarkdow(
            source_document=self.md_documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            headers_to_split_on=headers_to_split_on,
        )
        self.chunk_documents = self.chunk_object.chunk_documents
        return self

