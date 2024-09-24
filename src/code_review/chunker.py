import os
import json
import logging
from pathlib import Path
from llama_index.core.node_parser import CodeSplitter
from llama_index.readers.file import FlatReader
import languages

class ChunkExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def detectLanguage(self, filePath):
        extension = Path(filePath).suffix[1:].lower()
        return languages.languageExtensions.get(extension, 'unknown')

    def processRepos(self, root_folder):
        root_path = Path(root_folder)
        for repo_path in root_path.iterdir():
            if repo_path.is_dir():
                self.processRepo(repo_path)

    def processRepo(self, repo_path):
        chunk_folder = repo_path / "chunk_data"
        chunk_folder.mkdir(exist_ok=True)
        file_counter = 0

        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and file_path.parent != chunk_folder:
                file_counter = self.processFile(file_path, chunk_folder, file_counter)

    def processFile(self, file_path, chunk_folder, file_counter):
        try:
            language = self.detectLanguage(file_path)
            if language == 'unknown':
                self.logger.info(f"Skipping file with unknown language: {file_path}")
                return file_counter
            
            document = FlatReader().load_data(file_path)
            
            code_splitter = CodeSplitter(chunk_lines=100, language=language, max_chars=100000)
            nodes = code_splitter.get_nodes_from_documents(document)
            
            for node in nodes:
                chunk_file_path = chunk_folder / f"{file_counter}.json"
                chunk_file_path.write_text(node.to_json(), encoding="utf-8")
                file_counter += 1
            
            self.logger.info(f"Processed file: {file_path}")
            return file_counter
                
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}", exc_info=True)
            return file_counter

if __name__ == "__main__":
    base_path = Path("./cloned_repos")
    chunk_extractor = ChunkExtractor()
    chunk_extractor.processRepos(base_path)

    