from tqdm import tqdm
import time , typing
import requests
import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.box import SIMPLE_HEAVY
from pathlib import Path
import sys
from test_utils.debug import logger

# import the test_lib
from test_utils.test_lib import Sentiment , writeJSON, json

# import the data handling libs
import pandas as pd

# init console
console = Console()

# downloads and reads the datasets 
datasets = [
    "https://raw.githubusercontent.com/abrazinskas/FewSum/master/artifacts/amazon/gold_summs/test.csv",
    "https://raw.githubusercontent.com/abrazinskas/FewSum/master/artifacts/amazon/gold_summs/train.csv"
] 
filenames = [
    f"{Path().cwd() / 'test-data/dataset_1.csv'}",
    f"{Path().cwd() / 'test-data/dataset_2.csv'}",
]

def whichDataToAnalyse(again : bool,choices = ["1", "2"]) -> (str | typing.Any):
    if not again:
        console.print(
            Panel(
                "[yellow]1][/yellow] test-data/dataset_1.csv\n"
                "[yellow]2][/yellow] test-data/dataset_2.csv"
                ,title="✨ select a dataset to work with ✨",expand=False,box=SIMPLE_HEAVY
            )
        )
    def Ask() -> str:
        prompt = console.input(" 👉 ")
        return prompt
    ask = Ask()
    if ask in choices:
        return ask
    elif ask in [""]:
        whichDataToAnalyse(again=True)
    else:
        logger.warning(f"'{ask}' not in {choices} . Defaulting to '1'")
        return "1"

def Scroll(jsonStr) -> None:
    speed = console.input(f"Do you want to decrease the delay between the words ([cyan]the larger the value the more the delay[/cyan]) ? [grey][ default : '{0.1}' may be too slow ][/grey] ") or float('0.1')
    if float(speed) < 0.00001 or float(speed) > 0.1:
        logger.error("Delay value should be between 0.1 and 0.00001")
        sys.exit(0)
    console.print(Text.from_markup("[blink]⚠️ Emojis and other complex text fromats may not be displayed correctly ! [/blink]"))
    time.sleep(4)
    for char in jsonStr:
        print(char, end='', flush=True)
        time.sleep(float(speed))
    
# download them
def downloadDatasets(datas : list, log : bool) -> None:
    """ Loop through the list of `URLs` and download each file """
    for url,fileName in zip(datas, filenames):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        try:
            # Create a tqdm progress bar
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {Path(fileName).name}") as pbar:
                with open(fileName, 'wb') as f:
                    for data in response.iter_content(chunk_size=1024):
                        pbar.update(len(data))
                        f.write(data)
        except Exception as e:
            if log:
                logger.error(f"Unexpected error ! ({e})")
            sys.exit(0)
    if log:
        logger.success('Download complete ! 👍')
        # log all the path details to console
        logger.info(f'{[Path(Name).name for Name in filenames]} saved to {[Path(paths).parent.name+"/"+Path(paths).name for paths in filenames]}')

def AnalyzeMultipleTexts(
        all_reviews : list[str], log : bool, saveJson : bool, outputMode : str
) -> None:
    all_sents = [] # for all sentiments
    Big_Dict = {} # holding everything !
    if log:
        logger.debug(f"Retrieving all reviews ...")
    if log:
        logger.info("Analyzing multiple texts ... ")
    for revs in all_reviews:
        all_sents.append(Sentiment(revs).get()) # list of dicts
    if log and (len(all_reviews)) > 10: # size of list gt 10
        console.print(Text.from_markup("[blink] This may take some time ... ⌛ [/blink]"))
        time.sleep(3)
    
    # make the json output
    for revs, sents in zip(
        all_reviews,
        all_sents
    ):
        Big_Dict.update({
            revs : sents
        })
    
    # write the json
    if saveJson:
        if log:
            logger.info("Writing to json file (test_temp.json) ... 👍")
        try:
            writeJSON(
                {
                    "sentiments-from-file" :  Big_Dict,
                }
            )
            console.print(Text.from_markup(f"[blink]⚠️ Emojis may be converted to Unicode surrogate pairs when writing ![/blink]"))
            time.sleep(3)
        except Exception as e:
            if log:
                logger.error(f"Unexpected error ! ({e})")
            sys.exit(0)
    if outputMode in ["scroll"]:
        if log:
            logger.info("Initializing scrolling ... ")
        Scroll(
            json.dumps(
        {
            'sentiments-from-file' : Big_Dict,
        },indent=4, sort_keys=True
    )
        )
    elif outputMode in ["show"]:
        console.print_json(json.dumps(
            {
                'sentiments-from-file' : Big_Dict,
            },indent=4, sort_keys=True
        ))
    else:
        # hidden
        if log:
            logger.info("Output hidden . Nothing will be visible on the terminal . ")
# test the downloaded files
def testDatasets(filePaths : list, N : int, log : bool,saveJson : bool, outputMode : str) -> None:
    """ Analyze the external datasets """
    # download the data sets
    downloadDatasets(datasets , log)
    # Load the CSV files into a DataFrame
    dataDF_1 = pd.read_csv(f'{filePaths[0]}', sep='\t')
    dataDF_2 = pd.read_csv(f'{filePaths[1]}', sep='\t')

    dataDF = {
        "1" : dataDF_1,
        "2" : dataDF_2
    }
    # Display the first 'N' rows of the DataFrame and analyse sentiment
    revs = [rev for rev in dataDF.get(whichDataToAnalyse(again=False)).sample(N).get("rev1")]
    AnalyzeMultipleTexts(revs, log, saveJson, outputMode)

def testModel(text : str, log : bool, saveJson : bool, outputMode : str, numberOfRows : int) -> None:
    """ Analyze the the `model` using different types of data """
    if outputMode not in ["hidden", "scroll", "show"]:
        if log:
            logger.error(f"Invalid output mode : {outputMode} . Valid ones are {['hidden', 'scroll', 'show']} .")
        sys.exit(0)
    # debug line
    if log:
        logger.debug(f"Called 'sentzi-test.py {sys.argv[1:]}' ")
    
    if not Path(text).exists() and not Path(text).is_file() and not text.lower() in ["ext.data"]:
        if log:
            logger.info("Analyzing text ... ")
        sentDict = Sentiment(text).get()
        # write the json
        if saveJson:
            if log:
                logger.info("Writing to json file (test_temp.json) ... 👍")
            try:
                writeJSON(
                    {
                        "text-sentiment" : sentDict,
                    }
                )
                console.print(Text.from_markup(f"[blink]⚠️ Emojis may be converted to Unicode surrogate pairs when writing ![/blink]"))
                time.sleep(3)
            except Exception as e:
                if log:
                    logger.error(f"Unexpected error ! ({e})")
                sys.exit(0)
        if outputMode in ["scroll"]:
            if log:
                logger.info("Initializing scrolling ... ")
            Scroll(
                json.dumps(
                {
                    "text-sentiment" : sentDict,
                },indent=4, sort_keys=True
            ))
        elif outputMode in ["show"]:
            # print the json
            console.print_json(json.dumps(
                {
                    "text-sentiment" : sentDict,
                },indent=4, sort_keys=True
            ))
        else:
            # hidden
            if log:
                logger.info("Output hidden . Nothing will be visible on the terminal . ")
    elif Path(text).exists() and Path(text).is_file():
        if log:
            logger.info(f"File {text} exists ")
            logger.debug(f"Checking if {text} is of the format '.txt' ... ")
        # check if file is a text file
        if Path(text).suffix in [".txt"]:
            if log:
                logger.info(f"File {text} is a text file 👍")
            all_sents = [] # for all sentiments
            Big_Dict = {} # holding everything !
            if log:
                logger.debug(f"Retrieving all reviews from {text} ...")
            all_reviews = [ 
                rev.strip()
                for rev in 
                open(
                    text,
                    "r",
                    encoding="utf-8"
                )
            ]
            if log:
                logger.info("Analyzing multiple texts ... ")
            for revs in all_reviews:
                all_sents.append(Sentiment(revs).get()) # list of dicts
            if log and (Path(text).stat().st_size) > 2: # file greater then 2 bytes
                console.print(Text.from_markup("[blink] This may take some time ... ⌛ [/blink]"))
                time.sleep(3)
            
            # make the json output
            for revs, sents in zip(
                all_reviews,
                all_sents
            ):
                Big_Dict.update({
                    revs : sents
                })
            
            # write the json
            if saveJson:
                if log:
                    logger.info("Writing to json file (test_temp.json) ... 👍")
                try:
                    writeJSON(
                        {
                            "sentiments-from-file" :  Big_Dict,
                        }
                    )
                    console.print(Text.from_markup(f"[blink]⚠️ Emojis may be converted to Unicode surrogate pairs when writing ![/blink]"))
                    time.sleep(3)
                except Exception as e:
                    if log:
                        logger.error(f"Unexpected error ! ({e})")
                    sys.exit(0)
            if outputMode in ["scroll"]:
                if log:
                    logger.info("Initializing scrolling ... ")
                Scroll(
                    json.dumps(
                {
                    'sentiments-from-file' : Big_Dict,
                },indent=4, sort_keys=True
            )
                )
            elif outputMode in ["show"]:
                console.print_json(json.dumps(
                    {
                        'sentiments-from-file' : Big_Dict,
                    },indent=4, sort_keys=True
                ))
            else:
                # hidden
                if log:
                    logger.info("Output hidden . Nothing will be visible on the terminal . ")
            
        else:
            if log:
                logger.error("Only '.txt' format files are supported !")
            sys.exit(0)
    
    elif text in ["ext.data"]:
        testDatasets(
            filenames,
            numberOfRows,
            log,
            saveJson,
            outputMode
        )


            

        






