import fire
from parser_utils import *

def read_file_paths():
    with open('filepaths.txt','r') as f:
        content = f.readlines()
    content = [c.strip() for c in content]
    return content


FILES_TO_PARSE = read_file_paths()

def run(step):
    input = FILES_TO_PARSE[step-1]
    out_path = '/scratch/ayl316/ttml_mr_data/xml_jsons/'+input.split('/')[-1][:-4]+'.json'
    parse_zip(input, out_path)

def main(step):
    run(step)


if __name__ == "__main__":
    fire.Fire(main)

