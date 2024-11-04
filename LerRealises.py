import os
import pydriller
import argparse
import subprocess
from csv import reader
import csv
from pydriller import Repository
import git

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Extract process metrics')
    # ap.add_argument('C:/Users/Raissa/Desktop/moshi', required=True)
    ap.add_argument('path', help='path to the repository')
    ap.add_argument('--commits', required=True, help='csv with list of commits to compare commitA and commitB')
    ap.add_argument('--projectName', required=True)
    ap.add_argument('--absolutePath', required=True)
    ap.add_argument('--mode', required=True,help='mode - tag for commits with tag, csv - for csv of commits')
    args = ap.parse_args()

    #folder with repo: projectA and projectB

    # path = pydriller.Git(args.path)
    repo = git.Repo(args.path)
    tags = repo.tags


    if(args.mode == 'tag'):
        # csvPath = args.absolutePath +"results/" +args.projectName + "-results-processMetrics.csv"
        # f = open(csvPath, "w", newline='')
        # writer = csv.writer(f)  


        ck_jar_path = os.path.join(args.absolutePath, "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
        output_dir = os.path.join(args.absolutePath, "results")
        output_dir2 = os.path.join(args.absolutePath)
        os.makedirs(output_dir, exist_ok=True)

        results = []


        for tag in tags:
            print(f"Analisando tag: {tag.name}")
            commit = repo.commit(tag)
            repo.git.checkout(tag)

            command = [
                "java", "-jar", ck_jar_path,
                args.path,  
                "true",     
                "0",        
                "false",    
                output_dir  
            ]

            try:
                    subprocess.run(command, check=True)

                    metrics_file = os.path.join(output_dir2, "resultsclass.csv")
                    # metrics_dict = {}

                    with open(metrics_file, 'r') as f:
                        reader = csv.reader(f)
                        header = next(reader) 
                        for row in reader:
                            results.append([tag.name] + row)


                    print(f"Métricas CK geradas para a tag {tag.name} com sucesso.")
            except subprocess.CalledProcessError as e:
                    print(f"Erro ao executar CK para a tag {tag.name}: {e}")


        output_csv_path = os.path.join(output_dir, f"{args.projectName}_results.csv")
        with open(output_csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tag'] + header) 
            writer.writerows(results)

        print("Todos os resultados foram salvos em:", output_csv_path)

