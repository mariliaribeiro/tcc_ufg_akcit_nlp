import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import os
import asyncio

# Caminho do arquivo de log na raiz do projeto
LOG_FILE = Path(__file__).resolve().parents[2] / "processed_leaflets.log"

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.etl.pdf_and_markdown_pipeline import PdfAndMarkdownPipeline
from src.etl.chunks import HEADERS_TO_SPLIT_ON
from src.connection.chat_model import LLMModel
from src.etl.kg_from_text import KGFromText
from src.connection.embeddings import EmbeddingsModel

# Configurações
chunk_size = 400
chunk_overlap = 100
headers_to_split_on = HEADERS_TO_SPLIT_ON
provider = "google"
embedding_provider = "hf"
temperature = 0.7
max_tokens = None

figsize = (10, 8)
show_node_properties = False

async def process_all():
    # Carregar nomes já processados
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            processed_files = set(line.strip() for line in f)
    else:
        processed_files = set()

    pdf_files = list(Path(RAW_DATA_DIR).glob("*.pdf"))
    print(f"Encontrados {len(pdf_files)} arquivos PDF.")

    pdf_md_pipeline = PdfAndMarkdownPipeline()
    llm = LLMModel(
        provider=provider,
        temperature=temperature,
        max_tokens=max_tokens
    ).llm
    embedding = EmbeddingsModel(
        provider=embedding_provider,
    ).embeddings

    for pdf_path in pdf_files:
        FILE_NAME = pdf_path.name
        if FILE_NAME in processed_files:
            print(f"Já processado, pulando: {FILE_NAME}")
            continue
        PDF_FILE_PATH = pdf_path
        MD_FILE_PATH = Path(PROCESSED_DATA_DIR) / f"{FILE_NAME}.md"

        print(f"\nProcessando: {FILE_NAME}")
        try:
            # 1. Converter PDF para markdown
            pdf_md_pipeline.pdf_to_markdown(
                source_file_path=PDF_FILE_PATH,
                dest_dir_path=PROCESSED_DATA_DIR,
                encoding="utf-8"
            )

            # 2. Carregar markdown
            pdf_md_pipeline.load_markdown(
                source_file_path=MD_FILE_PATH
            )

            # 3. Gerar chunks
            pdf_md_pipeline.get_chunks(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                headers_to_split_on=headers_to_split_on,
            )

            # 4. Criar grafo de conhecimento
            kg = KGFromText(
                llm=llm,
                embeddings=embedding
            )

            chunk_documents = pdf_md_pipeline.chunk_documents
            await kg.get_kg(
                chunk_documents=chunk_documents
            )

            try:
                kg.plot_and_export_visualization(
                    file_name=FILE_NAME,
                    figsize=figsize, 
                    show_node_properties=show_node_properties,
                    show_plot=False
                )
            except Exception as viz_exc:
                print(f"[ERRO] Falha ao exportar visualização para {FILE_NAME}: {viz_exc}")

            try:
                kg.save()
            except Exception as save_exc:
                print(f"[ERRO] Falha ao salvar grafo no banco para {FILE_NAME}: {save_exc}")

            # 5. Registrar no log
            with open(LOG_FILE, 'a') as f:
                f.write(FILE_NAME + '\n')
            print(f"Processamento finalizado e registrado: {FILE_NAME}")
        except Exception as e:
            print(f"[ERRO] Falha ao processar {FILE_NAME}: {e}")

if __name__ == "__main__":
    asyncio.run(process_all()) 