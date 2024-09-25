from code_review.git_handler import *
from presentation_screening.evaluate_pitch import *
import csv

def download_repo(url: str, team_name, base_path="./data") -> None:
    git_handler = GitHandler()
    git_handler.clone_repository(url, team_name,base_path)
    
def savePresentation(ppt_url,team_name) -> None:
    presentation_analyser = PresentationAnalyser()
    presentation_analyser.save_file(ppt_url, team_name)
    
def save_both(url: str, team_name, ppt_url: str) -> None:
    download_repo(url, team_name)
    savePresentation(ppt_url, team_name)

def get_cloning_url(url: str) -> str:
    # Check if the URL contains '/tree/' or '/blob/'
    if '/tree/' in url:
        base_url = url.split('/tree/')[0]
    elif '/blob/' in url:
        base_url = url.split('/blob/')[0]
    else:
        base_url = url
    
    return base_url


def process_csv(input_csv: str, output_csv: str, base_path="./data") -> None:
    with open(input_csv, mode='r') as infile, open(output_csv, mode='a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        # next(reader)  # Skip header row
        for index, row in enumerate(reader, start=1):
            team_name, ppt_url, repo_url = row
            numbered_team_name = str(index)
            print(get_cloning_url(repo_url))
            save_both(get_cloning_url(repo_url), numbered_team_name, ppt_url)
            writer.writerow([team_name, numbered_team_name])

process_csv("src/team_data.csv", "src/team_data_output.csv")