from pypdf import PdfReader

from cognee.shared.logging_utils import get_logger
from cognee.modules.chunking.Chunker import Chunker
from cognee.infrastructure.files.utils.open_data_file import open_data_file

from .Document import Document
from .exceptions.exceptions import PyPdfInternalError

logger = get_logger("PDFDocument")


class PdfDocument(Document):
    type: str = "pdf"

    async def read(self, chunker_cls: Chunker, max_chunk_size: int):
        async with open_data_file(self.raw_data_location, mode="rb") as stream:
            logger.info(f"Reading PDF: {self.raw_data_location}")

            try:
                file = PdfReader(stream, strict=False)
            except Exception:
                raise PyPdfInternalError()

            async def get_text():
                try:
                    for page in file.pages:
                        page_text = page.extract_text()
                        yield page_text
                except Exception:
                    raise PyPdfInternalError()

            chunker = chunker_cls(self, get_text=get_text, max_chunk_size=max_chunk_size)

            async for chunk in chunker.read():
                yield chunk
