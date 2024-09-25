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
