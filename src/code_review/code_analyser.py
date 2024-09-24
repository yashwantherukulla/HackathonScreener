import os
import json
import time
import logging
from collections import defaultdict
from groq import Groq
import instructor
from code_file_eval_model import CodeReviewModel
import languages

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class CodeAnalyser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_code(self, file_path: str):
        with open(file_path, 'r') as f:
            code = f.read()
        return code

    def getOutput(self, filePath: str):
        sys_prompt = """
You are an expert code reviewer tasked with evaluating projects for a prestigious hackathon. Your mission is to provide comprehensive, insightful, and impartial reviews that will assist the judges in their final evaluation. Analyze the given code meticulously, considering the unique context of a hackathon environment.

## Core Evaluation Criteria:
1. Code Quality (readability, maintainability, consistency, commenting)
    - "readability": The code's adherence to best practices for readability (like following certain conventions or being consistant in naming, etc) and organization. If there is very less related to this in the code then you can give a lower score.,
    - "maintainability": The code's maintainability, including how easy it is to understand and modify. If the code is very complex and hard to understand then you can give a lower score.,
    - "consistency": The code's consistency in style, formatting, and structure. If the code is not consistent in style, formatting, and structure then you can give a lower score.,
    - "commenting": The code's commenting, including the presence of useful comments and documentation. If the code is not commented properly then you can give a lower score.
    
2. Functionality (correctness, completeness, error handling)
    - "correctness": The code's correctness, including the absence of bugs and errors. If the code has bugs and errors that you are 100 percent sure of, then you can give a lower score.,
    - "completeness": The code's completeness, including the presence of all required features and functionality. If the code is incomplete then you can give a lower score.,
    - "error_handling": The code's error handling, including how well it handles exceptions and edge cases. If the code does not handle exceptions and edge cases properly then you can give a lower score.,
    
3. Performance (efficiency, scalability)
    - "efficiency": The code's efficiency, including its performance and resource usage. If the code is not efficient then you can give a lower score.,
    - "scalability": The code's scalability, including its ability to handle increased load or data. If the code is not scalable then you can give a lower score.,
    
4. Security
    - "security": The code's security, including its vulnerability to attacks and data breaches. If the code is not secure then you can give a lower score.,
5. Testing (test coverage)
    - "test_coverage": The code's test coverage, including the percentage of code covered by tests. If the code has low test coverage then you can give a lower score.,
    
6. Innovation and Creativity
    - "innovation": The code's innovation, including its originality and creativity. If the code is not innovative then you can give a lower score.,
    - "creativity": The code's creativity, including its unique and novel solutions. If the code is not creative then you can give a lower score.,

7. Technical Complexity
    - "complexity_score": The code's complexity, if the code is too simple i.e., not sophisticated enough for the project then you can give a lower score.,
    - "technical_complexity": The code's technical complexity, including its advanced concepts and techniques. If the code is not technically complex then you can give a lower score.


## Guidelines for Review:
- Scores must be integers from 1 (poor) to 10 (excellent).
- "Lower Score" is less than five and "high score" is greater than five. Think of score 5 as neutral or average.
- Apply extremely harsh and rigorous standards in your evaluation, as these scores will determine the ultimate winner.
- For each code section, carefully consider its merits and shortcomings before assigning a score.
- Base your review exclusively on the provided code, making informed inferences about its context and purpose when necessary.
- Give special consideration to innovation, and technical complexity, keeping the hackathon context in mind.

## Review Process:
1. Thoroughly examine the entire codebase.
2. Evaluate each category (Code Quality, Functionality, etc.) individually.
3. Think of specific, actionable feedback for each category.
4. Identify key strengths and weaknesses.
5. Think of some concrete improvements.
6. Assess the overall technical complexity and innovation.
7. Based on all the analysis, assign scores to each category.

## Output Format:
Follow the provided model structure for your review. Ensure all fields are completed with thoughtful, detailed responses.

## Final Considerations:
- Your review will be a crucial tool for the hackathon judges. Ensure it provides a clear, comprehensive picture of the project's strengths, weaknesses, and potential.
- Consider the project's originality and potential impact in the field.

Remember, your evaluation could be the deciding factor in selecting groundbreaking projects. Approach this task with the utmost diligence and expertise.
        """

        client = Groq(api_key="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")
        client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

        output = client.chat.completions.create(
            model="llama-3.1-70b-versatile",#"mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": self.get_code(filePath),
                }
            ],
            response_model=CodeReviewModel,
        )
        return output

    def processRepos(self, root_folder):
        mapping = {}
        
        for repoName in os.listdir(root_folder):
            repoPath = os.path.join(root_folder, repoName)
            if os.path.isdir(repoPath):
                logging.info(f"Processing repo: {repoPath}")
                self.processRepo(repoPath, mapping)
                self.finalScores(repoPath)

        with open(os.path.join(repoPath, "file_output_mapping.json"), "w") as f:
            json.dump(mapping, f, indent=2)

    def processRepo(self, repoPath, mapping):
        outputFolder = os.path.join(repoPath, "output_data")
        os.makedirs(outputFolder, exist_ok=True)
        chunkFolderPath = os.path.join(repoPath, "chunk_data")
        for file in os.listdir(chunkFolderPath):
            filePath = os.path.join(chunkFolderPath, file)
            if os.path.isfile(filePath):
                logging.info(f"\tProcessing chunk: {filePath}")
                self.processChunk(filePath, outputFolder, mapping)
            time.sleep(0.75)

    def processChunk(self, filePath, outputFolder, mapping):
        try:
            output = self.getOutput(filePath).model_dump_json(indent=2)
            # get the filename without extension
            outputFilePath = os.path.join(outputFolder, f"{os.path.splitext(os.path.basename(filePath))[0]}.json")
            
            with open(outputFilePath, "w", encoding="utf-8") as f:
                f.write(output)
            
            mapping[filePath] = outputFilePath
        except Exception as e:
            self.logger.info(f"Error processing file {filePath}: {str(e)}")

    def finalScores(self, repoPath):
        directory = os.path.join(repoPath, "output_data")
        score_aggregation = defaultdict(int)
        files = 0

        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r') as file:
                    data = json.load(file)

                for key, value in data.items():
                    if isinstance(value, dict) and 'score' in value:
                        score_aggregation[key] += value['score']
            files += 1

        for category in score_aggregation:
            score_aggregation[category] = round(score_aggregation[category]/files)

        output_data = {
            "scores_by_category": dict(score_aggregation)
        }

        output_file = os.path.join(repoPath, "output_data/scores_summary.json")
        with open(output_file, 'w') as file:
            json.dump(output_data, file, indent=2)

        self.logger.info(f"Scores summary saved to: {output_file}")

if __name__ == "__main__":
    base_path = "./cloned_repos"
    code_analyser = CodeAnalyser()
    code_analyser.processRepos(base_path)